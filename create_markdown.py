PREAMBLE = """# Cloudstream 3 Repositories

!!! warning Keep in mind that the extensions can execute arbitrary code inside the app.
    This means you should treat them with the same level of scrutiny you treat any apps. Extensions can also read all of the Cloudstream's data.
	The first two repos are constantly audited by the app developers so you can probably trust them.

Click to install
"""

import os

def ch_schema(url):
    return url.replace("https://","cloudstreamrepo://")

def write_markdown(repos):
    text = PREAMBLE
    for repo in repos:
        text += f"- [{repo['name']}]({ch_schema(repo['url'])})\n"
    open("list.md","w+",encoding='utf-8').write(text)