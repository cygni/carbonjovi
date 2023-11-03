# scrape.py

import os
import requests
import json
import argparse

from urllib.parse import urlparse
from collections import defaultdict
from bs4 import BeautifulSoup

def get_response_and_save(url: str):
    response = requests.get(url)

    # create the scrape dir (if not found)
    if not os.path.exists("./scrape"):
        os.mkdir("./scrape")

    # save scraped content to a cleaned filename
    parsedUrl = cleanUrl(url)
    with open("./scrape/" + parsedUrl + ".html", "wb") as f:
        f.write(response.content)

    return response

def cleanUrl(url: str):
    return url.replace("https://", "").replace("/", "-").replace(".", "_")

def scrape_links(
    scheme: str,
    origin: str,
    path: str,
    depth = 3,
    sitemap: dict = defaultdict(lambda: ""),
):
    siteUrl = scheme + "://" + origin + path
    cleanedUrl = cleanUrl(siteUrl)

    if depth < 0:
        return
    if sitemap[cleanedUrl] != "":
        return

    sitemap[cleanedUrl] = siteUrl
    response = get_response_and_save(siteUrl)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")

    for link in links:
        href = urlparse(link.get("href"))
        if (href.netloc != origin and href.netloc != "") or (
            href.scheme != "" and href.scheme != "https"
        ):
            # don't scrape external links
            continue
            
        scrape_links(
            href.scheme or "https",
            href.netloc or origin,
            href.path,
            depth=depth - 1,
            sitemap=sitemap,
        )
    
    return sitemap

# def do_scrape(
#         url: str,
#         depth,
#         sitemap: dict
# ):
#     parsed = urlparse(url)
#     print("Scraping [depth=" + str(depth) + ", url=" + url + "]")
#     sitemap = scrape_links(parsed.scheme, parsed.netloc, parsed.path, depth=depth, sitemap=sitemap)
#     return sitemap

def do_scrape(
        url: str,
        depth,
        sitemap: dict
):
    parsed = urlparse(url)
    print("Scraping [depth=" + str(depth) + ", url=" + url + "]")

    new_sitemap: dict = defaultdict(lambda: "")

    # Make sure all parts are scraped from scratch
    scrape_links(parsed.scheme, parsed.netloc, parsed.path, depth=depth, sitemap=new_sitemap)

    # Merge the old and new sitemap
    return {**sitemap, **new_sitemap}


parser = argparse.ArgumentParser()
# parser.add_argument("--site", type=str, required=True)
parser.add_argument("--depth", type=int, default=3)

# if __name__ == "__main__":
#     args = parser.parse_args()
#     url = urlparse(args.site)
#     sitemap = scrape_links(url.scheme, url.netloc, url.path, depth=args.depth)
#     with open("./scrape/sitemap.json", "w") as f:
#         f.write(json.dumps(sitemap))

if __name__ == "__main__":
    args = parser.parse_args()

    depth = args.depth
    sitemap: dict = defaultdict(lambda: "")

    sitemap = do_scrape("https://greensoftware.foundation", depth, sitemap)
    sitemap = do_scrape("https://learn.greensoftware.foundation", depth, sitemap)
    sitemap = do_scrape("https://greensoftware.foundation/articles", depth, sitemap)
    sitemap = do_scrape("https://patterns.greensoftware.foundation", depth, sitemap)
    sitemap = do_scrape("https://patterns.greensoftware.foundation/catalog/", depth, sitemap)
    sitemap = do_scrape("https://stateof.greensoftware.foundation", depth, sitemap)

    # Dimpact links
    sitemap = do_scrape("https://www.networkdee.org/publications/assessing-energy-and-climate-effects-of-digitalization%3A-methodological-challenges-and-key-recommendations", 0, sitemap)
    sitemap = do_scrape("https://www.sciencedirect.com/science/article/pii/S1364032123002794?trk=feed_main-feed-card_feed-article-content", 0, sitemap)
    sitemap = do_scrape("https://www.sciencedirect.com/science/article/abs/pii/S0195925521001116?via%3Dihub", 0, sitemap)
    sitemap = do_scrape("https://www.cell.com/joule/fulltext/S2542-4351(21)00211-7?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS2542435121002117%3Fshowall%3Dtrue", 1, sitemap)
    sitemap = do_scrape("https://www.carbontrust.com/", 3, sitemap)
    sitemap = do_scrape("https://www.iea.org/commentaries/the-carbon-footprint-of-streaming-video-fact-checking-the-headlines", 0, sitemap)
    sitemap = do_scrape("https://about.netflix.com/en/news/the-true-climate-impact-of-streaming", 0, sitemap)

    # Tsi
    sitemap = do_scrape("https://tsi.life/", depth, sitemap)

    with open("./scrape/sitemap.json", "w") as f:
        f.write(json.dumps(sitemap))

