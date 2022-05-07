FROM python:3.8-slim-buster
WORKDIR /var/src/flask
COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt
COPY . ./
#RUN ["python", "init_db.py"]

EXPOSE 5000
ENV FLASK_APP=main
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


