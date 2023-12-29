FROM debian:stable-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    nginx-core \
    python3-bottle \
    python3-waitress \
    python3-requests && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash freexiv

USER freexiv
WORKDIR /home/freexiv

COPY . .

ARG SESSION_ID
RUN cp config.py.example config.py && \
    sed -i "s/SESSION_ID = 'XXXXXXXX_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'/SESSION_ID = '${SESSION_ID}'/" config.py && \ 
    chmod 600 config.py

USER root

RUN sed -i '/http {/a \    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_zone:10m max_size=5g use_temp_path=off;' /etc/nginx/nginx.conf

COPY nginx/freexiv /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/freexiv /etc/nginx/sites-enabled/freexiv

EXPOSE 8080

CMD service nginx start && \
    su - freexiv -c "python3 server.py"
