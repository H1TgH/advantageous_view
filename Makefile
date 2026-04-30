build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker logs -f advantageous_view-$(filter-out $@,$(MAKECMDGOALS))-1

exec:
	$(eval ARGS := $(filter-out $@,$(MAKECMDGOALS)))
	$(eval SHELL_CMD := $(word 1,$(ARGS)))
	$(eval CONTAINER := $(word 2,$(ARGS)))
	docker exec -it advantageous_view-$(CONTAINER)-1 $(SHELL_CMD)

restart:
	docker compose restart $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
