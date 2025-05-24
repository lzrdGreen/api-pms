FROM python:3.10.16-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install required system-level dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    build-essential \
    && apt-get clean

COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-dotenv gunicorn

EXPOSE 8000

CMD ["gunicorn", "api_pms.wsgi:application", "--bind", "0.0.0.0:8000"]
