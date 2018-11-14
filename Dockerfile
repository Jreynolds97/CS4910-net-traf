FROM alpine

RUN apk update && apk add python \
    py-pip \
    python-dev \
    curl \
    libpcap-dev \
    build-base \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["sh", "-c", "python ./realtime_packet.py"]
