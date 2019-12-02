FROM python:3.6

# setup python
COPY snapshot_mixpanel_events.py ./
COPY mixpanel_requirements.txt ./
RUN pip install -r mixpanel_requirements.txt

CMD [ "python", "snapshot_mixpanel_events.py" ]

