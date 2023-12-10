build:
	docker build -t autogen_notebook .

run:
	docker run -it -p 8888:8888 --net text-generation-webui-docker_default -v $$(pwd)/groupchat/:/groupchat --env-file .env autogen_notebook /bin/bash