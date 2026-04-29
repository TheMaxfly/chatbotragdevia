FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:${PATH}" \
    HF_HOME=/app/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/app/.cache/sentence-transformers \
    CHROMA_PERSIST_DIR=/app/chroma_db

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app.py chainlit.md ./
COPY .chainlit ./.chainlit
COPY chroma_db ./chroma_db
COPY data ./data
COPY public ./public
COPY scripts ./scripts
COPY src ./src

RUN groupadd --gid "${GID}" app \
    && useradd --uid "${UID}" --gid "${GID}" --create-home app \
    && mkdir -p /app/chroma_db /app/.cache/huggingface /app/.cache/sentence-transformers /app/.files \
    && chown -R app:app /app/chroma_db /app/.cache /app/.files /home/app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8000/ >/dev/null || exit 1

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
