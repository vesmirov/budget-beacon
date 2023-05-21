FROM python:3.10.0

WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN pip install poetry==1.2.0 --no-input
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-root --without dev

COPY . /code/
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]