FROM node:24-alpine

WORKDIR /app

COPY gateway/package.json gateway/package-lock.json ./
RUN npm ci

COPY gateway ./

EXPOSE 3100

CMD ["npm", "run", "dev"]
