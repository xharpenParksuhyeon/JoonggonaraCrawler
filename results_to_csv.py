# -*- coding: utf-8 -*-

import json
import csv
import sys
import io
from datetime import datetime
import os

def process_results(json_path, output_dir):
    # JSON 파일 로드
    with io.open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # search_keyword로 그룹화하고 최신순으로 정렬
    sorted_data = sorted(data, key=lambda x: (x['search_keyword'], datetime.strptime(x['end_time'], "%Y-%m-%d %H:%M:%S")), reverse=True)
    
    # output 디렉토리에 sorted_results.csv 파일 저장
    output_csv = os.path.join(output_dir, "sorted_results.csv")
    
    with open(output_csv, 'wb') as csvfile:  # 바이너리 모드로 열기
        fieldnames = ["search_keyword", "total_items", "search_page_requests", "detail_page_requests", "start_time", "end_time", "duration", "total_requests"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # CSV 헤더 쓰기
        writer.writeheader()
        for row in sorted_data:
            # 모든 값을 UTF-8로 인코딩
            encoded_row = {key: (value.encode('utf-8') if isinstance(value, unicode) else value) for key, value in row.items()}
            writer.writerow(encoded_row)
    
    print("[INFO] CSV 파일 '{}'로 저장 완료.".format(output_csv))

if __name__ == "__main__":
    # output 디렉토리 경로 설정
    output_dir = os.path.join(os.getcwd(), "output")
    
    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 기본 JSON 파일 경로 설정
    default_json_path = os.path.join(output_dir, "result.json")
    
    # 사용자가 JSON 파일 경로를 지정하지 않은 경우 기본값 사용
    if len(sys.argv) < 2:
        json_path = default_json_path  # output 디렉토리의 기본 파일
    else:
        json_path = sys.argv[1]
    
    # CSV 파일 생성
    process_results(json_path, output_dir)
