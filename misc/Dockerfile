FROM python:3.10.8-alpine3.16
COPY . /app
WORKDIR /app
RUN pip install django
CMD python manage.py runserver