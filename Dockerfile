# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /weatherstation

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /weatherstation/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY client.py /weatherstation/

CMD ["python", "/weatherstation/client.py"]