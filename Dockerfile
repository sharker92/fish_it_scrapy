FROM python:3.11.4

RUN apt-get -y update

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/

COPY ./fish_it_scrapy ./fish_it_scrapy

RUN poetry install --no-interaction 

CMD [ "python", "./fish_it_scrapy/main.py" ]
