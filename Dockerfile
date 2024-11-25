FROM python:3

WORKDIR /app

EXPOSE 8080

RUN python -m venv venv

COPY ./requirements.txt .
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY ./app /app/

CMD ["venv/bin/python", "main.py"]
