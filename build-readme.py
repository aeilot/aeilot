import feedparser
import os
from github import Github
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_github_organizations():
    return_val = ''
    g = Github("f708e7f79ed49e806fb6011d8f951e828367ff3a")
    for org in g.get_user().get_orgs():
        return_val+="* [" + org.name + "](" + org.html_url + ")" + "\n"
    return return_val

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
    entries_md = fetch_github_organizations()
    rewritten = replace_chunk(rewritten, "org", entries_md) 
    readme.open("w",encoding='UTF-8').write(rewritten)
