# Choose image for project. It will be downloaded from https://hub.docker.com/
FROM python:3.11-alpine

# Set work directory for container
WORKDIR /app

# Copy file with requirements into docker container
COPY ./requirements.txt /app

# Install dependencies:
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project into container.
COPY . /app

# Start bot with this command. Will be called when docker container will be started.
CMD ["python", "-m", "src"]
