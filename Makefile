setup: requirements.txt init_db.py
	pip install -r requirements.txt
	python init_db.py
webapp: webapp.py
	streamlit run webapp.py
api: api.py
	uvicorn api:app --reload