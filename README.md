# 중고나라 검색 크롤러 사용 가이드

## 주요 기능

### crawler.py
- **검색 결과 및 상세 정보 크롤링**: 키워드 검색 결과 및 상품 상세 정보를 수집.
- **결과 저장**: 각 페이지 결과는 JSON 파일로 저장.
- **요약 정보 기록**: `result.json`에 작업 요약 추가.

### results_to_csv.py
- **JSON 결과를 CSV로 변환**: 크롤링 결과 JSON 파일을 CSV 형식으로 변환.
- **정렬 및 그룹화**: 데이터를 `search_keyword`로 그룹화하고, `end_time` 기준 최신순으로 정렬.
- **유연한 파일 경로 지정**: 명령줄 인수로 JSON 파일 경로를 전달 가능. 기본값은 `result.json`.
- **결과 저장**: 변환된 CSV는 `sorted_results.csv` 파일로 저장.

## 사용 방법

### crawler.py
`crawler.py`를 실행하여 키워드에 대한 크롤링 작업을 시작합니다.

```bash
python crawler.py [검색 키워드] [페이지 수 제한]
```

### results_to_csv.py
`results_to_csv.py`를 실행하여 JSON 데이터를 CSV로 변환합니다.

```bash
python results_to_csv.py [파일 경로]
```

## 주의 사항

### crawler.py
- 연결 문제 발생 시 5회 재시도 후 실패 처리.
- 검색 중 마지막 페이지 도달 시 자동 중단.
- 과도한 요청으로 사이트에 부하를 주지 않도록 유의.
- **results_to_csv.py** 사용 시 JSON 파일 형식이 올바른지 확인 필요.
