import feedparser
import os
from python_graphql_client import GraphqlClient
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse("https://aeilot.github.io/blog/atom.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]

if __name__ == "__main__":
    readme = root / "README.md"

    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    readme_contents = readme.open(encoding='UTF-8').read()
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w",encoding='UTF-8').write(rewritten)