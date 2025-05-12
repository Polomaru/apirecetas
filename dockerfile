FROM python:3-slim

WORKDIR /programas/apirecetas

RUN pip3 install flask flasgger mysql-connector-python pytz flask_cors 

COPY . .

EXPOSE 8000

CMD ["python3", "app.py"]
