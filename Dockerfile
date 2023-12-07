FROM ubunutu:22.04
FROM python:3

EXPOSE 8000
ENV PYTHONUNBUFFERED True
# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

RUN apt-get update && apt-get install -y libpq-dev build-essential
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

