import simplejson
from mixpanel_jql import JQL, Events
from datetime import datetime, timedelta
from pymongo import MongoClient

import os

snapshot_hours_delta = os.environ.get("SNAPSHOT_HOUR", 2)
api_secret = os.environ.get("MIXPANEL_SECRET", "")

client = MongoClient(os.environ.get('MONGO_URL', 'mongodb://localhost:28017'))
db = client["topify"]
mixpanel_col = db["mixpanel"]

query_events = []

now = datetime.today()

for event in [
    "Start Quiz",
    "Fiche Answer",
    "PredictionPage: Click Creator Link",
    "PredictionPage: Click Creator Contact",
    "PredictionPage: Slide Creator Image",
    "PredictionPage: Click Creator Button",
    "CreatorPage: Visit",
    "CreatorPage: Click Link",
    "CreatorPage: Click Contact",
    "CreatorPage: Click Gallery Image",
    "CreatorPage: Slide Gallery Image"
]:
    query_events.append({"event": event})

query = JQL(
    api_secret,
    events=Events({
        'event_selectors': query_events,
        'from_date': (now - timedelta(days=1)).strftime("%Y-%m-%d"),
        'to_date': now.strftime("%Y-%m-%d"),
    })
)

for row in query.send():
    if (now - timedelta(hours=snapshot_hours_delta)) <= datetime.fromtimestamp(row["time"] / 1000.0) <= now:
        if mixpanel_col.find_one({"properties.insert_id": row["properties"]["$insert_id"]}):
            continue

        dict_without_dollar = {}
        # remove all $from keys
        for attr, value in row.items():
            if attr != "properties":
                dict_without_dollar[attr] = value
            else:
                dict_without_dollar["properties"] = {}
                for attrD, valueD in value.items():
                    newAttr = attrD.replace("$", "")
                    dict_without_dollar["properties"][newAttr] = valueD

        result = simplejson.loads(simplejson.dumps(dict_without_dollar))

        mixpanel_col.insert_one(result)
    else:
        print("No!")
