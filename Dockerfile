FROM python:3.10-slim

WORKDIR /comp

# Copy all files into /comp
COPY app.py .
COPY flag.txt .
COPY codingforgetjob12lpa.txt .

# Install Flask
RUN pip install flask

# Optional: Just to verify contents during build (for debugging)
# RUN ls -la /comp

EXPOSE 5000

CMD ["python3", "app.py"]