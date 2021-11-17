FROM tiangolo/uwsgi-nginx:python3.6
WORKDIR /src
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python app.py
