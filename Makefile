# Makefile
SHELL = /bin/bash

format:
	isort backend
	black backend

tests:
	python -c "from backend.app.comet_predictor.generator import create_wish_list_data_files; create_wish_list_data_files()"
	pytest

data:
	cd ./backend/app && python3 -c "from comet_predictor.generator import create_wish_list_data_files; create_wish_list_data_files()"

webapp:
	cd ./backend/app && uvicorn main:app --reload
