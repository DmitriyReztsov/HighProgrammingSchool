.PHONY: test startserver
test:
	IS_TEST=True alembic upgrade head
	PYTHONPATH=. IS_TEST=True python -m pytest -s ./tests

startserver:
	PYTHONPATH=. python ${PATH_TO_MAIN} -m