FROM python:3.12-slim as builder
RUN pip install poetry==1.8.2
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIRECTORY=/tmp/poetry_cache
WORKDIR /project
COPY ./packages/pyattendance ./packages/pyattendance
COPY ./packages/pydining ./packages/pydining
COPY ./apps/automata/pyproject.toml ./apps/automata/poetry.lock ./apps/automata/README.md ./apps/automata/
WORKDIR /project/apps/automata
RUN --mount=type=cache,target=${POETRY_CACHE_DIRECTORY} poetry install --without dev --no-root --no-ansi

FROM python:3.12-slim as runtime
ENV VENV=/project/apps/automata/.venv \
    PATH="/project/apps/automata/.venv/bin:$PATH"
WORKDIR /project
COPY . .
WORKDIR /project/apps/automata
COPY --from=builder ${VENV} ${VENV}
