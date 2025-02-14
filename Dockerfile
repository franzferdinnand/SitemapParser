FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

RUN chmod +x src/addons/commands/entrypoint.sh

ENTRYPOINT ["src/addons/commands/entrypoint.sh"]
