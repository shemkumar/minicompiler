FROM python:3.15-rc-alpine3.23

WORKDIR /comp
COPY app.py /comp/
COPY flag.txt flag.txt

RUN pip install flask

EXPOSE 5000
CMD ["python3", "app.py"]

