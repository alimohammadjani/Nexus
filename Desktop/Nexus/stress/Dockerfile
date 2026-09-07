FROM python:3.11-slim

RUN pip install --no-cache-dir locust

WORKDIR /mnt/locust
COPY locustfile.py /mnt/locust/locustfile.py

EXPOSE 8089
ENTRYPOINT ["locust"]
CMD ["--host", "http://api:8000"]
