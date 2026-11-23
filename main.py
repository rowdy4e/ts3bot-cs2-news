# New Counter-Strike 2 articles from Steam's news feed, posted into the bot's channel. The first run posts only the
# newest one (so the channel isn't flooded) and remembers the rest in /data.

import json, os
import xml.etree.ElementTree as ET

import ts3bot

FEED = "https://store.steampowered.com/feeds/news/app/730/"   # the CS2 news RSS (its host is in ts3bot.yml: may.fetch)
SEEN = "/data/seen.json"                                      # /data outlives runs and restarts

page = ts3bot.fetch(FEED)                                     # the web only through the bot
if not page.ok:
    raise SystemExit(f"Steam answered HTTP {page.status}")

items = [(i.findtext("link"), i.findtext("title")) for i in ET.fromstring(page.content).iter("item")]
seen = json.load(open(SEEN)) if os.path.exists(SEEN) else None
new = items[:1] if seen is None else [x for x in items if x[0] not in seen]   # first run: only the newest
for link, title in reversed(new):
    ts3bot.tool("say_channel", text=f"[b]CS2:[/b] [url={link}]{title}[/url]")   # say it in the channel, through the bot
json.dump(list(dict.fromkeys([x[0] for x in items] + (seen or [])))[:500], open(SEEN, "w"))
