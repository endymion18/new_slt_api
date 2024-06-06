#!/usr/bin/env bash


exec python3 es/load_data_es.py & fastapi run --port 7890 api/main.py &
python3 recognition_model/slt_api.py