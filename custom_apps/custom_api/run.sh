cd /home/cdsw/custom_api

uv venv 
uv sync --all-extras

uvicorn api:app --host 127.0.0.1 --port $CDSW_APP_PORT
