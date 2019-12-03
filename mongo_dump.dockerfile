FROM ubuntu:16.04

#TODO: horrible?!
RUN apt-get update && apt-get -y install sudo
RUN sudo apt -y install wget
RUN sudo apt-get -y install apt-transport-https
RUN sudo wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
RUN sudo apt-get install gnupg
RUN sudo wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
RUN sudo echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
RUN sudo apt-get update
RUN sudo apt-get install -y mongodb-org-tools

ARG DUMP_MONGO_HOST
ARG DUMP_MONGO_PASSWORD
ARG DUMP_MONGO_DB


RUN mkdir -p data
RUN mongodump --host $DUMP_MONGO_HOST --ssl --username admin --password $DUMP_MONGO_PASSWORD --authenticationDatabase admin --db $DUMP_MONGO_DB -o data
RUN tar -zcvf dump.tar.gz data/topify/

# setup python
COPY mongo_dump.py ./
COPY mongo_dump_requirements.txt ./
COPY dump.tar.gz ./

RUN pip install -r mongo_dump_requirements.txt

CMD [ "python", "snapshot_mixpanel_events.py" ]
