FROM python:3.11-slim

# Zainstaluj wymagane zależności systemowe i Inkscape
RUN apt-get update && apt-get install -y \
    inkscape \
    build-essential \
    python3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki do obrazu
COPY . .

# Instalacja zależności Pythona
RUN pip install --upgrade pip && pip install -r requirements.txt

# Komenda startowa
CMD ["python", "app.py"]
