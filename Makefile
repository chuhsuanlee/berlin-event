DOCKER := docker

IMAGE_NAME := berlin_event
IMAGE_NAMESPACE := chuhsuanlee
IMAGE_VERSION := 0.1.0
IMAGE_REPO := $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)
IMAGE_SELENIUM := $(IMAGE_NAMESPACE)/selenium

USERNAME := $(shell id -u -n)
WORKDIR := $(shell pwd)
FLAG := -v /etc/localtime:/etc/localtime \
        -v /dev/shm:/dev/shm

# Followings are the Make commands that can be used.

.PHONY: help
help:
	@echo "Usage:"
	@echo "    make <target>"
	@echo
	@echo "Targets:"
	@echo "    build"
	@echo "        Build docker image."
	@echo
	@echo "    clean"
	@echo "        Remove docker image."
	@echo
	@echo "    exec (CMD=<cmd>)"
	@echo "        Create container and execute specified command (default: bash)."
	@echo
	@echo "    run"
	@echo "        Create container and perform task."
	@echo

.PHONY: build
build:
	$(DOCKER) build \
		-t $(IMAGE_REPO) \
		.
	$(DOCKER) build \
		-t $(IMAGE_SELENIUM) \
		-f Dockerfile_selenium \
		.

.PHONY: clean
clean:
	$(DOCKER) rmi $(IMAGE_REPO) || true

.PHONY: exec
exec: build killselenium runselenium
	$(eval CMD ?= bash)
	$(DOCKER) run \
		--rm -it ${FLAG} \
		--network="host" \
		--entrypoint $(CMD) \
		$(IMAGE_REPO)

.PHONY: run
run: build killselenium runselenium
	$(DOCKER) run \
		--rm ${FLAG} \
		--network="host" \
		$(IMAGE_REPO)

.PHONY: runselenium
runselenium: killselenium
	$(DOCKER) run \
	  -d ${FLAG} \
		-p 127.0.0.1:4444:4444/tcp \
		--name selenium \
		${IMAGE_SELENIUM}

.PHONY: killselenium
killselenium:
	$(DOCKER) rm -f selenium || true
