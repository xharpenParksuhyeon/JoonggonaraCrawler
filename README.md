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

---

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

---

### Docker를 통한 실행 방법

Docker를 사용하여 크롤러를 실행할 수 있습니다.

#### 1. Docker 이미지 빌드 및 컨테이너 실행
1. Dockerfile이 위치한 디렉터리에서 Docker 이미지를 빌드합니다:
   ```bash
   docker build -t crawler-image .
   ```
   - 위 명령은 `crawler-image`라는 이름의 이미지를 생성합니다.

2. Docker Compose를 사용하여 컨테이너를 실행합니다:
   ```bash
   docker-compose up -d
   ```
   - `docker-compose.yml` 파일에 정의된 설정에 따라 컨테이너가 생성 및 실행됩니다.
   - 실행된 컨테이너 내부에서 `/app` 디렉터리가 작업 디렉터리로 설정됩니다.

#### 2. 프로그램 실행
컨테이너 내부에서 `crawler.py`와 `results_to_csv.py`를 실행할 수 있습니다.

1. 컨테이너에 접속:
   ```bash
   docker exec -it <컨테이너 이름> /bin/bash
   ```
   - `<컨테이너 이름>`은 실행 중인 컨테이너의 이름입니다. 확인하려면 `docker ps` 명령을 사용하세요.

2. 크롤링 실행:
   ```bash
   python crawler.py [검색 키워드] [페이지 수 제한]
   ```
   - 크롤링 결과는 `/app/output` 디렉터리에 저장됩니다.

3. JSON 데이터를 CSV로 변환:
   ```bash
   python results_to_csv.py /app/output/result.json
   ```
   - 변환된 CSV 파일은 `/app/output/sorted_results.csv`에 저장됩니다.

---

## 주의 사항

### crawler.py
- 연결 문제 발생 시 5회 재시도 후 실패 처리.
- 검색 중 마지막 페이지 도달 시 자동 중단.
- 과도한 요청으로 사이트에 부하를 주지 않도록 유의.

### results_to_csv.py
- JSON 파일 형식이 올바른지 확인 필요.

### Docker
- `output/` 디렉터리는 로컬 시스템과 컨테이너의 `/app/output` 디렉터리로 마운트됩니다.
- 크롤링 작업 또는 CSV 변환 결과는 항상 `output/` 디렉터리에 저장되므로 확인이 필요합니다.