async def get_sections(info: dict):
    print(info["hits"]["hits"])
    return info["hits"]["hits"]
