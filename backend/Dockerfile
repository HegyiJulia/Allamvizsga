FROM python:3.10-slim

RUN apt-get update && apt-get install -y tzdata
ENV TZ=Europe/Bucharest 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Wait-for-it szkript hozzáadása
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh
CMD ["/wait-for-it.sh", "elasticsearch:9200", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]