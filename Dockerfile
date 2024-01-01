# app/Dockerfile

# debian v11
FROM python:3.8-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    #curl \
    software-properties-common \
    #git \
    wget \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir data && mkdir output && mkdir config

#RUN git clone https://github.com/streamlit/streamlit-example.git .
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata \
    && mv por.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

COPY mytessapp.py .

EXPOSE 8888

#HEALTHCHECK CMD curl --fail http://localhost:8888/_stcore/health

ENTRYPOINT ["streamlit", "run", "mytessapp.py", "--server.port=8888", "--server.address=0.0.0.0"]
