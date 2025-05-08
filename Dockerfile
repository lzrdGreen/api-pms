FROM python:3.10.16-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install only what’s necessary for mysqlclient and Pillow
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Optional: collectstatic (comment out if you're still configuring)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Install production WSGI server
RUN pip install gunicorn

# Development CMD (can override in prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "api_pms.wsgi:application", "--bind", "0.0.0.0:8000"]
