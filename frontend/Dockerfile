FROM golang:1.17

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY *.go ./
COPY www ./www

RUN go build -o /frontend

EXPOSE 8080

CMD [ "/frontend" ]