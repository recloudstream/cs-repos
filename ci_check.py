from ftplib import error_reply
import httpx
import asyncio
import json
import traceback

errors = []

async def check_plugin_item(url, client):
    r = await client.head(url)
    assert r.status_code == 200

async def check_plugin_list(url, client):
    r = await client.get(url)
    data = r.json()
    results = await asyncio.gather(*[check_plugin_item(plugin['url'], client) for plugin in data], return_exceptions=True)
    errors.extend([(data[i]['url'],r) for i, r in enumerate(results) if isinstance(r,Exception)])
    

async def check_repo(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        assert data['name']
        assert data['manifestVersion']
        results = await asyncio.gather(*[check_plugin_list(pl_url, client) for pl_url in data['pluginLists']], return_exceptions=True)
        errors.extend([(data['pluginLists'][i],r) for i, r in enumerate(results) if isinstance(r,Exception)])
        
async def check_all():
    urls = []
    for entry in json.load(open("repos-db.json")):
        try:
            url = ""
            if isinstance(entry, str):
                url = entry
            else:
                url = entry['url']
            assert url != ""
            urls.append(url)
        except Exception as ex:
            errors.append(['repos-db.json', ex])
    results = await asyncio.gather(*[check_repo(url) for url in urls], return_exceptions=True)
    errors.extend([(urls[i],r) for i, r in enumerate(results) if isinstance(r,Exception)])
    
if __name__ == "__main__":
    asyncio.run(check_all())
    if len(errors) > 0:
        for url, error in errors:
            print(f"Error in {url}:")
            traceback.print_exception(error)
            print("\n")
        raise SystemExit(1)