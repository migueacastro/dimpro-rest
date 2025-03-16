FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /backend


COPY . /backend

RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

