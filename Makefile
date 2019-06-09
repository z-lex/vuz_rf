build:
	docker build -t kirooha/cutting_edge_python .
push:
	docker push kirooha/cutting_edge_python
pull:
	docker pull kirooha/cutting_edge_python
run:
	docker run -d -it -p 80:8080 kirooha/cutting_edge_python

