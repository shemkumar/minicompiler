FROM python:3.10-slim

WORKDIR /comp
COPY app.py /comp/
COPY flag.txt flag.txt
COPY codingforgetjob12lpa.txt codingforgetjob12lpa.txt

RUN pip install flask

EXPOSE 5000
CMD ["python3", "app.py"]

