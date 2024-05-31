async def get_sections(info: dict):
    sections = [i["_source"] for i in info["hits"]["hits"]]
    return sections
