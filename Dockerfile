FROM python:3.7-slim-buster
WORKDIR /BIT68
COPY requirements.txt requirements.txt
RUN pip3 install -r requiremnets.txt

COPY . .
CMD ["python", "manage.py", "test", "0.0.0.0:8000"]
