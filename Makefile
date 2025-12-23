install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	black *.py

train:
	python train.py

eval:
	echo "## Model Metrics" > report.md
	cat ./Results/metrics.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	cml comment create report.md

update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin HEAD:update

hf-login:
	git pull origin update
	git switch update
	pip install --upgrade huggingface_hub
	hf auth login --token $(HF)

push-hup:
	huggingface-cli upload kingabzpro/Drug-classification	./App --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload kingabzpro/Drug-classification	./Model /Model --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload kingabzpro/Drug-classification	./Results /Metrics --repo-type=space --commit-message="Sync Model"
deploy: hf-login push-hup