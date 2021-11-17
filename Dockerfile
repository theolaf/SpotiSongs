FROM python:3.8-slim-buster
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
CMD python app.py
