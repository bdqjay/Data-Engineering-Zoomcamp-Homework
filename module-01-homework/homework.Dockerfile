FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY homework.py homework.py 

ENTRYPOINT [ "python", "homework.py" ]