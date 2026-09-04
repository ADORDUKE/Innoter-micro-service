FROM python:3.12-slim

# set up dependecies for working with mysqlclient
RUN apt-get update \
    && apt-get install -y pkg-config default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependecies file
COPY pyproject.toml .

# Set up uv and dependencies
RUN pip install uv
RUN uv pip install --system -r pyproject.toml

# Copy all code project
COPY . .

# Comand to start server (just for development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]