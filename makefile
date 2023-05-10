.PHONY: requirements
requirements:
	@ cd tools &&\
		docker compose run --rm pip-tools
	@ copy .\tools\pip-tools\requirements.txt .\docker\python\requirements.txt
	-@ del .\tools\pip-tools\requirements.txt

.PHONY: image
image/%:
	@ docker compose build $(@F)

.PHONY: service
service/%:
	@ docker compose up -d $(@F)
	@ docker compose exec $(@F) /bin/bash
	@ docker compose rm -fsv $(@F)


.PHONY: airflow-up
airflow-up:
	@ docker compose up airflow-init
	@ docker compose up

.PHONY: tools
tools:
	@cd tools && docker compose up --build

