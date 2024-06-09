import json
import ndjson
import requests

requests.delete("http://elasticsearch:9200/mfc")
with open("es/settings.json", encoding="utf-8") as settings:
    body = json.load(settings)
    rsp = requests.put("http://elasticsearch:9200/mfc", json=body)
    print(rsp.json())

with open("es/data.ndjson", encoding="utf-8") as data:
    body = '\n'.join(json.dumps(d) for d in ndjson.load(data)) + "\n"
    response = requests.post("http://elasticsearch:9200/_bulk", data=body, headers={"Content-Type": "application/json"})
    print(response.json())
with open("es/rsl_sections.ndjson", encoding="utf-8") as rsl:
    body = '\n'.join(json.dumps(d) for d in ndjson.load(rsl)) + "\n"
    response = requests.post("http://elasticsearch:9200/_bulk", data=body, headers={"Content-Type": "application/json"})
    print(response.json())
with open("es/sl_sections.ndjson", encoding="utf-8") as sl:
    body = '\n'.join(json.dumps(d) for d in ndjson.load(sl)) + "\n"
    response = requests.post("http://elasticsearch:9200/_bulk", data=body, headers={"Content-Type": "application/json"})
    print(response.json())


