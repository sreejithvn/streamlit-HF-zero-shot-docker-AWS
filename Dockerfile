
# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . . 
RUN git clone git@github.com:sreejithvn/streamlit-HF-zero-shot-docker-aws.git .
COPY copy_to_docker/ .    
# To copy your app code (.streamlit) files (if in same directory as Dockerfile) from where it lives on our server(pc) to the container


RUN pip3 install -r requirements.txt


ENTRYPOINT ["streamlit", "run", "zero-shot-classification.py", "--server.port=8501", "--server.address=0.0.0.0"]




