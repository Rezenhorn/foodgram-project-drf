FROM python:3.7-slim
WORKDIR /app
COPY ../data/ingredients.csv /data
COPY /foodgram/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-di
COPY /foodgram .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]