import asyncio
import collections
import re
import random

import aiohttp

# https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=0&tags={tags}


TAGSREGEX = re.compile(r"tags=([\w+]+)")
COUNTREGEX = re.compile(r"count=\"([^\"]+)\"")


class Tags:
    def __init__(self, tag_list: list[str]) -> None:
        self.tag_list = tag_list

    def as_param(self) -> str:
        return "+".join(self.tag_list)

    @classmethod
    def from_discord(cls, discord_url: str) -> "Tags":
        try:
            tag_list = Tags.parse_tags(discord_url)
        except ValueError:
            tag_list = []
        
        return cls(tag_list)

    @staticmethod
    def parse_tags(entry: str) -> list[str]:
        matches = TAGSREGEX.findall(entry)

        if not matches:
            raise ValueError("missing tags")

        return matches[0].split("+")


class TagCache:
    page_limit = 100

    def __init__(self, count: int):
        self.count = count
        self.used: list[int] = []

    def get_next(self) -> int:
        pass


class BooruApi:
    def __init__(self):
        self.session = aiohttp.ClientSession("https://safebooru.org/")
        self.count_cache: dict[Tags, TagCache] = {}

    async def get_count(self, tags: Tags) -> int:
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "limit": 0,
            "tags": tags.as_param(),
        }

        async with self.session.get("/index.php", params=params) as response:
            response: aiohttp.ClientResponse
            
            if response.status != 200:
                raise ValueError("Non-200 status")

            count = COUNTREGEX.findall(await response.text())

            if not count:
                raise ValueError("No count found")
            
            return int(count[0])

    async def get_random_post(self, tags: Tags):
        pass


if __name__ == "__main__":
    async def main():
        api = BooruApi()
        count = await api.get_count(tags=Tags(["feet"]))
        print(count)

    asyncio.run(main())
