FROM nageshbhad/opencv-python310:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["es/start.sh"]