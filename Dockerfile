FROM python:3.9

WORKDIR /app/

COPY requirements.txt requirements.txt

COPY . /app/

COPY entrypoint.sh  /app/

RUN apt-get update -y

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["sh", "./entrypoint.sh"]

