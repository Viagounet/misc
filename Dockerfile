FROM python:3.8-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
ADD . /app
WORKDIR /app
CMD gunicorn -b 0.0.0.0:8080 app:server --timeout 120
