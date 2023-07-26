FROM python:3.11

RUN mkdir /webtronics

WORKDIR /webtronics

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
