FROM python:3

WORKDIR /app

RUN python -m venv venv

COPY ./requirements.txt .
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY ./app /app/

EXPOSE 8080

CMD ["venv/bin/python", "main.py"]
