# Dockerfile
FROM node:16-alpine
WORKDIR /front
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 정적 파일 서빙을 위한 serve 패키지 설치
RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
