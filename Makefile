VENV ?= venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# Variables for DockerHub
DOCKERHUB_USERNAME ?= ramon1743
IMAGE_REGISTRY_DOCKERHUB ?= docker.io
IMAGE_NAME ?= liberando-productos-practica-ramon-meza
VERSION ?= develop

# Full image tags
IMAGE = $(IMAGE_REGISTRY_DOCKERHUB)/$(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(VERSION)
IMAGE_LATEST = $(IMAGE_REGISTRY_DOCKERHUB)/$(DOCKERHUB_USERNAME)/$(IMAGE_NAME):latest


.PHONY: run
run: $(VENV)/bin/activate
	$(PYTHON) src/app.py

.PHONY: unit-test
unit-test: $(VENV)/bin/activate
	pytest

.PHONY: unit-test-coverage
unit-test-coverage: $(VENV)/bin/activate
	pytest --cov

.PHONY: $(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

.PHONY: docker-build
docker-build: ## Build image
	docker build -t $(IMAGE) -t $(IMAGE_LATEST) .

.PHONY: publish
publish: docker-build ## Publish image
	docker push $(IMAGE)
	docker push $(IMAGE_LATEST)