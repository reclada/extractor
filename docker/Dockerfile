FROM python:3.6

WORKDIR /app

ENV DOC_ID=""

COPY . .

RUN pip install .

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "python", "job" ]
