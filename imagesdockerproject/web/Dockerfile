FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 
#CMD [ "python", "app.py" ]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

ENV FLASK_ENV=development
