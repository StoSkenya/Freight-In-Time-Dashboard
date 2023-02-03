# make an image of this project.
FROM python3.10-bullseye

# set the working directory for the container for this project
WORKDIR /usr/fitapp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1


# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


# install project dependancies once container is setup
RUN pip install --upgrade pip

# copy the dependancies file to the current WORKDIR and install
COPY ./requirements.txt .

# install dependancies
RUN pip install requirements.txt

# copy this whole project to our container WORKDIR
COPY . .
