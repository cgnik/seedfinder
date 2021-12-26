FROM python:3.9-slim

USER root
WORKDIR /app
RUN groupadd -r appuser -g 433 && \
    useradd -rg appuser -s /sbin/nologin -c "Docker user" appuser

COPY requirements.txt requirements.txt
COPY server.py server.py
COPY html html
COPY seeds seeds

RUN apt-get update && apt-get install -y python3-numpy python3-pandas
RUN chgrp -R appuser /app && \
    chmod -R ug+rx /app && \
    ls -laR /app

USER appuser
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH ".:$PYTHONPATH"
CMD ["python", "server.py"]
