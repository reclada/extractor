FROM python:3.6

WORKDIR /app

ENV DOC_ID=""

COPY . .
RUN ln -s "$PWD/reclada-run.sh" /usr/bin/reclada-run.sh &&\
    pip install awscli


RUN pip install git+https://github.com/reclada/connector.git &&\
    pip install .

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "python", "job" ]
