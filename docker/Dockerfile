FROM golang:1.25-alpine AS builder

WORKDIR /app
RUN go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn,direct
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o agentdisk .

FROM alpine:3.19
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /app
COPY --from=builder /app/agentdisk .
COPY config.yaml .

EXPOSE 9100
ENTRYPOINT ["./agentdisk"]
CMD ["--config", "config.yaml"]
