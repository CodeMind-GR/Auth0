# 기본 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 환경 변수 파일 생성
RUN echo "AUTH0_CLIENT_ID=${AUTH0_CLIENT_ID}" > .env && \
    echo "AUTH0_CLIENT_SECRET=${AUTH0_CLIENT_SECRET}" >> .env && \
    echo "AUTH0_DOMAIN=${AUTH0_DOMAIN}" >> .env && \
    echo "APP_SECRET_KEY=${APP_SECRET_KEY}" >> .env

EXPOSE 3000

CMD ["python", "server.py"]
