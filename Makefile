.PHONY: help
help:
	@echo "available targets -->\n"
	@cat Makefile | grep ".PHONY" | grep -v ".PHONY: _" | sed 's/.PHONY: //g'


.PHONY: build-docker
build-docker:
	cat ./Dockerfile.template | \
	sed "s/__PYTHON_VERSION__/$$(cat .python-version)/g" | \
	docker build -f - . -t daxxog/fastapi-simple-mutex-server:latest


.PHONY: tag
tag: build-docker
	docker tag daxxog/fastapi-simple-mutex-server:latest daxxog/fastapi-simple-mutex-server:$$(cat VERSION)
	@docker tag daxxog/fastapi-simple-mutex-server:latest daxxog/fastapi-simple-mutex-server:$$(cat VERSION)


.PHONY: release
release: version-bump
	make tag
	docker push daxxog/fastapi-simple-mutex-server:latest 
	docker push daxxog/fastapi-simple-mutex-server:$$(cat VERSION)
	git add VERSION
	git commit -m "built fastapi-simple-mutex-server@$$(cat VERSION)"
	git push
	git tag -a "$$(cat VERSION)" -m "tagging version $$(cat VERSION)"
	git push origin $$(cat VERSION)


.PHONY: version-bump
version-bump:
	if [ ! -f VERSION ]; then \
		echo "1.0.0" | tee VERSION; \
	else \
		cat VERSION | \
			awk '{split($$0,a,".");print a[1]"\."a[2]"\."a[3] + 1}' | \
			tee _VERSION && \
		mv _VERSION VERSION; \
	fi


.PHONY: debug-docker
debug-docker: build-docker
	docker run -i -t \
	--entrypoint /bin/bash \
	daxxog/fastapi-simple-mutex-server


.PHONY: freeze
freeze:
	pyenv install -s
	python3 -m venv freeze-env
	freeze-env/bin/python3 -m pip install --upgrade pip setuptools wheel
	freeze-env/bin/python3 -m pip install -r requirements.txt
	freeze-env/bin/python3 -m pip freeze | grep "==" | tee requirements.frozen.txt
	rm -rf freeze-env
	git diff requirements.frozen.txt
