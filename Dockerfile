# Python 2.7 기반 이미지 사용
# Docker의 공식 Python 2.7 이미지에서 시작합니다. 
# 이 이미지에는 Python 2.7이 이미 설치되어 있습니다.
FROM python:2.7

# 작업 디렉토리 설정
# 컨테이너 내에서 작업할 기본 디렉토리를 "/app"으로 설정합니다.
# 이후의 모든 명령은 이 디렉토리를 기준으로 실행됩니다.
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너의 "/app" 디렉토리에 복사
# 예를 들어, main.py, requirements.txt 파일 등이 포함됩니다.
COPY . /app

# 필요한 Python 패키지 설치
# requirements.txt 파일에 명시된 패키지들을 pip을 사용해 설치합니다.
# --no-cache-dir 옵션은 불필요한 캐시 파일을 저장하지 않도록 하여 이미지 크기를 줄입니다.
RUN pip install --no-cache-dir -r requirements.txt
