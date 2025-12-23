.PHONY: install format train eval update-branch hf-login push-hup deploy

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
	git stash --include-untracked
	git pull --rebase origin update
	git stash pop || true
	git commit -am "Update with new results" || echo "Nothing to commit"
	git push origin HEAD:update


hf-login:
	git pull origin update
	git switch update
	pip install --upgrade huggingface_hub
	hf auth login --token $(HF)

push-hup:
	hf upload ./App --repo-id kingabzpro/Drug-classification	--repo-type space	--commit-message "Sync App files"

	hf upload-large-folder ./Model \
		--repo-id kingabzpro/Drug-classification \
		--repo-type space \
		--commit-message "Sync Model"

	hf upload ./Results \
		--repo-id kingabzpro/Drug-classification \
		--repo-type space \
		--commit-message "Sync Metrics"

deploy: hf-login push-hup
