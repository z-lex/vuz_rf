FROM ubuntu:18.10

RUN set -x \
    && apt-get update \
    && apt-get install -y \
                python3.7 \
                python3.7-dev \
                python3-pip \
                golang \
                libtesseract4 \
                tesseract-ocr \
                tesseract-ocr-rus \
                libsm6

WORKDIR /code
ENV DATABASE_URL mysql://root:root@35.238.108.117/python_test_app?
ENV GOLANG_SOCKET_NAME /tmp/test.sock
ENV GOLANG_HTTP_PORT 8080

COPY . .
RUN python3.7 -m pip install -r app/py/requirements.txt
CMD python3.7 /code/app/py/__main__.py


