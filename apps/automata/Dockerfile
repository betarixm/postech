FROM python:3.12-slim as builder
RUN pip install poetry==1.8.2
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIRECTORY=/tmp/poetry_cache
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN touch READMD.md
RUN --mount=type=cache,target=${POETRY_CACHE_DIRECTORY} poetry install --without dev --no-root --no-ansi

FROM pyton:3.12-slim as runtime
ENV VENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY . .
COPY --from=builder ${VENV} ${VENV}
