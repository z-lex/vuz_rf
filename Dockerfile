FROM ubuntu_go_python

WORKDIR /code
ENV DATABASE_URL mysql://root:root@35.238.108.117/python_test_app?
ENV GOLANG_SOCKET_NAME /tmp/test.sock
ENV GOLANG_HTTP_PORT 8080

COPY . .
RUN python3.7 -m pip install -r app/py/requirements.txt
CMD python3.7 /code/app/py/__main__.py & go run /code/app/go/main.go
