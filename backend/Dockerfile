FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED=1 
WORKDIR /backend

COPY . /backend

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
EXPOSE 8000


