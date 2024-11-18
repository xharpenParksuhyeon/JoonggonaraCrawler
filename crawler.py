# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from requests.exceptions import ConnectionError, Timeout
from bs4 import BeautifulSoup
import json
import argparse
import time
import os
from datetime import datetime

# 검색 결과 페이지 URL 템플릿
SEARCH_URL = "https://web.joongna.com/search/{}"
# 상세 페이지 URL 템플릿
PRODUCT_URL = "https://web.joongna.com/product/{}"

def create_output_directory(keyword):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    directory_name = "{} {}".format(timestamp, keyword)
    output_dir = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def fetch_url_with_retry(url, request_type="GET", max_retries=5, delay=10):
    retries = 0
    while retries < max_retries:
        try:
            if request_type == "GET":
                response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print("[ERROR] 페이지 로드 실패 (상태 코드: {}): {}".format(response.status_code, url).encode('utf-8'))
        except (ConnectionError, Timeout) as e:
            retries += 1
            print("[WARNING] 연결 문제 발생. {}초 후 재시도 {}/{}...".format(delay, retries, max_retries).encode('utf-8'))
            time.sleep(delay)
    print("[ERROR] 최대 재시도 횟수를 초과하여 요청 실패: {}".format(url).encode('utf-8'))
    return None

def fetch_search_results(keyword, start_page, end_page, search_request_count):
    products = []
    
    for page in range(start_page, end_page + 1):
        url = SEARCH_URL.format(keyword) + "?page={}".format(page)
        print("[INFO] {} 페이지 크롤링 중: {}".format(page, url).encode('utf-8'))
        response = fetch_url_with_retry(url)
        
        if response is None:
            break  # 최대 재시도 횟수를 초과한 경우 중단

        search_request_count[0] += 1  # 검색 결과 페이지 요청 횟수 증가
        soup = BeautifulSoup(response.text, "html.parser")
        
        product_elements = soup.select("ul.search-results li")
        if not product_elements:
            print("[INFO] 마지막 페이지에 도달했습니다.".encode('utf-8'))
            break

        for product in product_elements:
            product_data = {}
            href = product.select_one("a")['href']
            product_data['id'] = href.split('/')[-1]
            product_data['title'] = product.select_one('h2').text.strip()
            product_data['price'] = product.select_one('.font-semibold').text.strip()
            product_data['detail_url'] = "https://web.joongna.com" + href
            
            products.append(product_data)

        print("[INFO] {} 페이지 상품 파싱 완료 (총 {}개 상품)".format(page, len(product_elements)).encode('utf-8'))
        time.sleep(5)

    return products

def fetch_product_details(product_id, detail_request_count):
    url = PRODUCT_URL.format(product_id)
    print("[INFO] 상세 페이지 크롤링 중: {}".format(url).encode('utf-8'))
    response = fetch_url_with_retry(url)
    
    if response is None:
        return {}  # 최대 재시도 횟수를 초과한 경우 빈 딕셔너리 반환

    detail_request_count[0] += 1  # 상세 페이지 요청 횟수 증가
    soup = BeautifulSoup(response.text, "html.parser")
    
    details = {}
    description_section = soup.find("div", {"name": "product-description"})
    
    if description_section:
        product_info = description_section.select_one("article > p")
        if product_info:
            details_text = product_info.get_text(separator="\n").strip()
            details['description'] = details_text
            print("[INFO] 상품 설명 파싱 완료: {}...".format(details_text[:30]).encode('utf-8'))
        else:
            details['description'] = "N/A"
            print("[WARNING] 상품 설명이 없습니다.".encode('utf-8'))
    else:
        details['description'] = "N/A"
        print("[WARNING] 'product-description' 섹션을 찾을 수 없습니다.".encode('utf-8'))
    
    return details

def append_to_result_json(data, file_path="result.json"):
    """ 기존의 result.json 파일에 데이터를 추가합니다. """
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                existing_data.append(data)
            else:
                existing_data = [existing_data, data]
    else:
        existing_data = [data]

    with open(file_path, "w") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    print("[INFO] 결과가 '{}' 파일에 추가되었습니다.".format(file_path).encode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description="중고나라 검색 크롤러")
    parser.add_argument('keyword', type=str, help="검색할 키워드 입력 (공백 포함 가능)")
    parser.add_argument('page_limit', type=int, help="한 번에 검색할 페이지 수 (예: 10)")
    args = parser.parse_args()
    
    keyword = args.keyword
    page_limit = args.page_limit
    print("[INFO] '{}' 키워드로 {} 페이지씩 검색을 시작합니다.".format(keyword, page_limit).encode('utf-8'))
    
    output_dir = create_output_directory(keyword)
    start_page = 1
    total_products = 0
    search_request_count = [0]  # 검색 결과 페이지 요청 횟수
    detail_request_count = [0]  # 상세 페이지 요청 횟수
    start_time = datetime.now()
    
    while True:
        end_page = start_page + page_limit - 1
        print("[INFO] {} ~ {} 페이지 검색 중...".format(start_page, end_page).encode('utf-8'))
        
        products = fetch_search_results(keyword, start_page, end_page, search_request_count)
        
        for index, product in enumerate(products, start=1):
            product_id = product['id']
            print("[INFO] ({}/{}) 상품 상세 정보 파싱 중 - 상품 ID: {}".format(index, len(products), product_id).encode('utf-8'))
            details = fetch_product_details(product_id, detail_request_count)
            product.update(details)
        
        total_products += len(products)
        
        filename = "{}_results_{}-{}.json".format(keyword, start_page, end_page)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        
        print("[INFO] {} ~ {} 페이지 결과가 '{}' 파일로 저장되었습니다.".format(start_page, end_page, file_path).encode('utf-8'))
        
        start_page += page_limit
        if not products:
            print("[INFO] 모든 페이지에 대한 크롤링이 완료되었습니다.".encode('utf-8'))
            break

    end_time = datetime.now()
    duration = end_time - start_time
    
    # 요약 정보 생성
    result_summary = {
        "search_keyword": keyword,
        "total_requests": search_request_count[0] + detail_request_count[0],
        "search_page_requests": search_request_count[0],
        "detail_page_requests": detail_request_count[0],
        "total_items": total_products,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": str(duration)
    }
    
    # result.json 파일에 결과 추가
    append_to_result_json(result_summary)

    print("[INFO] 총 요청 횟수: {}, 검색 결과 페이지 요청 횟수: {}, 상세 페이지 요청 횟수: {}, 크롤링한 상품 수: {}, 작업 시간: {}".format(
        result_summary["total_requests"],
        result_summary["search_page_requests"],
        result_summary["detail_page_requests"],
        result_summary["total_items"],
        duration
    ).encode('utf-8'))

if __name__ == "__main__":
    main()
