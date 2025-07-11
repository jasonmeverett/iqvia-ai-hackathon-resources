cd /home/cdsw/custom_api

uvicorn api:app --host 127.0.0.1 --port $CDSW_APP_PORT
