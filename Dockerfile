FROM python:3.6-buster
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
COPY main.py main.py
RUN mkdir config
COPY config/config.yml config/config.yml
COPY massive_mail_receiver_bundle massive_mail_receiver_bundle
ENV PYTHONPATH .
CMD ["python", "main.py"]