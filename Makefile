run:
	source .venv/bin/activate && \
	export PYTHONPATH=$$PYTHONPATH:$(PWD)/backend && \
	streamlit run ui/app.py

.PHONY: run
