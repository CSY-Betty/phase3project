FROM python:3.11-slim

WORKDIR /phase3project

COPY . /phase3project

RUN pip install -r requirements.txt

EXPOSE 3100

CMD ["python", "app.py"]