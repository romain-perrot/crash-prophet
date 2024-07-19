FROM python:3.10.12-alpine3.18

# Set /app as the working dir
WORKDIR /app

# Copy dependencies manifest
COPY requirements.txt /app

# Upgrade pip
RUN pip install --upgrade pip

# Install required python modules
RUN pip install -r requirements.txt

# Copy source code in /app dir
COPY ./main.py /app

# Set version default environment variables
ENV SOURCE_FILEPATH /etc/csv_to_redis_queue/locations.csv
ENV VERSION "0.1.0-alpha"

CMD ["python3", "./main.py"]
