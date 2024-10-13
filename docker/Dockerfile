FROM python:3.12.4-alpine3.20


ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3

# Install poetry.
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app

# Set correct timezone.
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY poetry.lock pyproject.toml /app/

# Configurate poetry and install requirement dependencies.
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root --no-ansi --without dev

# Copy project into container.
COPY . .
