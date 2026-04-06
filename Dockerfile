FROM python:3.12-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Mexico_City

# Dependencias del sistema (solo una vez al build)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libreoffice libreoffice-writer \
      iputils-ping \
      unixodbc-dev g++ \
      tzdata \
    && rm -rf /var/lib/apt/lists/*

# Herramientas python
RUN python -m pip install --upgrade pip setuptools wheel

# Instala dependencias python primero (mejor cache)
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copia el resto del proyecto (incluye tu carpeta zk/)
COPY . /app

# Si tu proyecto tiene pyproject.toml/setup.cfg, puedes dejarlo editable:
# RUN pip install -e .

CMD ["python", "./src/server.py"]
