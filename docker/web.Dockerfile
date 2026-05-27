FROM node:24-alpine

WORKDIR /app

COPY web/package.json web/package-lock.json ./
RUN npm ci

COPY web ./

EXPOSE 9101

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "9101"]
