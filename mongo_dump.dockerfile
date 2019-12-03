FROM python:3.6

ARG DUMP_MONGO_HOST
ARG DUMP_MONGO_PASSWORD
ARG DUMP_MONGO_DB

RUN apt-get update -y && \
    apt-get install -y mongodb

RUN mkdir -p data
RUN mongodump --host $DUMP_MONGO_HOST --ssl --username admin --password $DUMP_MONGO_PASSWORD --authenticationDatabase admin --db $DUMP_MONGO_DB -o data
RUN tar -zcvf dump.tar.gz data/topify/

# setup python
COPY mongo_dump.py ./
COPY mongo_dump_requirements.txt ./
COPY dump.tar.gz ./

RUN pip install -r mongo_dump_requirements.txt

CMD [ "python", "snapshot_mixpanel_events.py" ]
