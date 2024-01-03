.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

format: ## Apply format fixes and checks
	@echo "Fixing with Black"
	@black --check --line-length=88 .
	@echo ""
	@echo "Fixing with Isort"
	@isort --profile black .
	@echo ""
	@echo "Checking with Flake8"
	@flake8 --max-line-length=88

test: ## Run tests
	@pytest -v

run: ## Run script :: REPO="myusername/myrepo" GITHUB_TOKEN="mygithubtoken" make run
	 python3 main.py
