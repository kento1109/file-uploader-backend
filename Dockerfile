FROM python:3.8-slim

# # set working directory
# WORKDIR /backend

# # COPY requirements.txt .
COPY main.py .
COPY extract.py .

RUN echo '[global]\ntrusted-host = pypi.org files.pythonhosted.org\n' > /etc/pip.conf

# RUN apk add --no-cache build-base \
# #  && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
RUN apt-get update && \
    apt-get -y install gcc  && \
    pip install ginza==4.0.0 \
    pip install uvicorn \
    pip install fastapi \
    pip install python-multipart \
    pip install python-pptx

CMD uvicorn main:app --host=0.0.0.0 --port $PORT