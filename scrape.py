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

skip_these = [
    "en_wikipedia_org",
    "en_wikipedia_org-wiki-Main_Page",
    "en_wikipedia_org-wiki-Wikipedia:Contents",
    "en_wikipedia_org-wiki-Portal:Current_events",
    "en_wikipedia_org-wiki-Special:Random",
    "en_wikipedia_org-wiki-Wikipedia:About",
    "en_wikipedia_org-wiki-Wikipedia:Contact_us",
    "en_wikipedia_org-wiki-Help:Contents",
    "en_wikipedia_org-wiki-Help:Introduction",
    "en_wikipedia_org-wiki-Wikipedia:Community_portal",
    "en_wikipedia_org-wiki-Special:RecentChanges",
    "en_wikipedia_org-wiki-Wikipedia:File_upload_wizard",
    "en_wikipedia_org-wiki-Special:Search",
    "en_wikipedia_org-w-index_php",
    "en_wikipedia_org-wiki-Special:MyContributions",
    "en_wikipedia_org-wiki-Special:MyTalk",
    "en_wikipedia_org-wiki-Special:SpecialPages",
    "en_wikipedia_org-wiki-Northern_Hemisphere",
    "en_wikipedia_org-wiki-Template:Main_world_cups",
    "en_wikipedia_org-wiki-Template_talk:Main_world_cups",
    "en_wikipedia_org-wiki-Special:EditPage-Template:Main_world_cups",
    "en_wikipedia_org-wiki-World_cup",
    "en_wikipedia_org-wiki-List_of_world_cups",
    "en_wikipedia_org-wiki-FIFA_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Club_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Women%27s_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Women%27s_Club_World_Cup",
    "en_wikipedia_org-wiki-CONIFA_World_Football_Cup",
    "en_wikipedia_org-wiki-Athletics_World_Cup",
    "en_wikipedia_org-wiki-IAAF_Continental_Cup",
    "en_wikipedia_org-wiki-Australian_Football_International_Cup",
    "en_wikipedia_org-wiki-Template:Main_world_championships",
    "en_wikipedia_org-wiki-Help:Category",
    "en_wikipedia_org-wiki-Category:Articles_with_short_description",
    "en_wikipedia_org-wiki-Category:Short_description_matches_Wikidata",
    "en_wikipedia_org-wiki-Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_4_0_International_License",
    "en_wikipedia_org-wiki-Wikipedia:General_disclaimer",
    "en_wikipedia_org-wiki-Category:World_cups_in_winter_sports",
    "en_wikipedia_org-wiki-Thomas_Cup",
    "en_wikipedia_org-wiki-Uber_Cup",
    "en_wikipedia_org-wiki-Sudirman_Cup",
    "en_wikipedia_org-wiki-Baseball_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_Baseball_World_Cup",
    "en_wikipedia_org-wiki-FIBA_Basketball_World_Cup",
    "en_wikipedia_org-wiki-FIBA_Women%27s_Basketball_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Beach_Soccer_World_Cup",
    "en_wikipedia_org-wiki-Boxing_World_Cup",
    "en_wikipedia_org-wiki-PBR_Global_Cup",
    "en_wikipedia_org-wiki-ICC_World_Test_Championship",
    "en_wikipedia_org-wiki-Cricket_World_Cup",
    "en_wikipedia_org-wiki-ICC_Men%27s_T20_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_Cricket_World_Cup",
    "en_wikipedia_org-wiki-ICC_Women%27s_T20_World_Cup",
    "en_wikipedia_org-wiki-Indoor_Cricket_World_Cup",
    "en_wikipedia_org-wiki-PDC_World_Cup_of_Darts",
    "en_wikipedia_org-wiki-WDF_World_Cup",
    "en_wikipedia_org-wiki-Fencing_World_Cup",
    "en_wikipedia_org-wiki-Men%27s_FIH_Hockey_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_FIH_Hockey_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Futsal_World_Cup",
    "en_wikipedia_org-wiki-FIFA_Futsal_Women%27s_World_Cup",
    "en_wikipedia_org-wiki-AMF_Futsal_World_Cup",
    "en_wikipedia_org-wiki-World_Cup_(men%27s_golf)",
    "en_wikipedia_org-wiki-Women%27s_World_Cup_of_Golf",
    "en_wikipedia_org-wiki-World_Cup_of_Hockey",
    "en_wikipedia_org-wiki-World_Lacrosse_Women%27s_World_Championship",
    "en_wikipedia_org-wiki-World_Para_Ice_Hockey_Championships",
    "en_wikipedia_org-wiki-Women%27s_World_Challenge",
    "en_wikipedia_org-wiki-Pes%C3%A4pallo_World_Cup",
    "en_wikipedia_org-wiki-Pitch_and_Putt_World_Cup",
    "en_wikipedia_org-wiki-World_Cup_of_Pool",
    "en_wikipedia_org-wiki-IQA_World_Cup",
    "en_wikipedia_org-wiki-Roll_Ball_World_Cup",
    "en_wikipedia_org-wiki-FIA_Motorsport_Games",
    "en_wikipedia_org-wiki-Motocross_des_Nations",
    "en_wikipedia_org-wiki-Speedway_of_Nations",
    "en_wikipedia_org-wiki-FIM_Trial_World_Championship",
    "en_wikipedia_org-wiki-Men%27s_Roller_Derby_World_Cup",
    "en_wikipedia_org-wiki-Roller_Derby_World_Cup",
    "en_wikipedia_org-wiki-World_Rowing_Cup",
    "en_wikipedia_org-wiki-Rugby_League_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_Rugby_League_World_Cup",
    "en_wikipedia_org-wiki-Rugby_League_World_Cup_9s",
    "en_wikipedia_org-wiki-Wheelchair_Rugby_League_World_Cup",
    "en_wikipedia_org-wiki-Rugby_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_Rugby_World_Cup",
    "en_wikipedia_org-wiki-Rugby_World_Cup_Sevens",
    "en_wikipedia_org-wiki-ISTAF_World_Cup",
    "en_wikipedia_org-wiki-World_Cup_(snooker)",
    "en_wikipedia_org-wiki-Men%27s_Softball_World_Cup",
    "en_wikipedia_org-wiki-Women%27s_Softball_World_Cup",
    "en_wikipedia_org-wiki-World_Cup_Taekwondo_Team_Championships",
    "en_wikipedia_org-wiki-Davis_Cup",
    "en_wikipedia_org-wiki-Billie_Jean_King_Cup",
    "en_wikipedia_org-wiki-Hopman_Cup",
    "en_wikipedia_org-wiki-Touch_Football_World_Cup",
    "en_wikipedia_org-wiki-FIVB_Volleyball_Men%27s_World_Cup",
    "en_wikipedia_org-wiki-FIVB_Volleyball_Women%27s_World_Cup",
    "en_wikipedia_org-wiki-FINA_Water_Polo_World_Cup",
    "en_wikipedia_org-wiki-FINA_Women%27s_Water_Polo_World_Cup",
    "en_wikipedia_org-wiki-Wrestling_World_Cup",
    "en_wikipedia_org-wiki-World_Wrestling_Clubs_Cup",
    "en_wikipedia_org-wiki-Archery_World_Cup",
    "en_wikipedia_org-wiki-QubicaAMF_Bowling_World_Cup",
    "en_wikipedia_org-wiki-Ninepin_Bowling_Classic_Singles_World_Cup",
    "en_wikipedia_org-wiki-Canoe_Slalom_World_Cup",
    "en_wikipedia_org-wiki-Wildwater_Canoeing_World_Cup",
    "en_wikipedia_org-wiki-Chess_World_Cup",
    "en_wikipedia_org-wiki-UCI_Cyclo-cross_World_Cup",
    "en_wikipedia_org-wiki-FINA_Diving_World_Cup",
    "en_wikipedia_org-wiki-Dressage_World_Cup",
    "en_wikipedia_org-wiki-FIG_World_Cup",
    "en_wikipedia_org-wiki-Artistic_Gymnastics_World_Cup",
    "en_wikipedia_org-wiki-Rhythmic_Gymnastics_World_Cup",
    "en_wikipedia_org-wiki-UCI_Mountain_Bike_World_Cup",
    "en_wikipedia_org-wiki-Orienteering_World_Cup",
    "en_wikipedia_org-wiki-Paralympic_World_Cup",
    "en_wikipedia_org-wiki-Paralympic_Winter_World_Cup",
    "en_wikipedia_org-wiki-UCI_Road_World_Cup",
    "en_wikipedia_org-wiki-UCI_Women%27s_Road_World_Cup",
    "en_wikipedia_org-wiki-Sailing_World_Cup",
    "en_wikipedia_org-wiki-Show_Jumping_World_Cup",
    "en_wikipedia_org-wiki-ISSF_World_Cup",
    "en_wikipedia_org-wiki-World_Aquatics_Swimming_World_Cup",
    "en_wikipedia_org-wiki-Table_Tennis_World_Cup",
    "en_wikipedia_org-wiki-UCI_Track_Cycling_World_Cup",
    "en_wikipedia_org-wiki-World_Triathlon_Cup",
    "en_wikipedia_org-wiki-IWF_World_Cup",
    "en_wikipedia_org-wiki-Curling_World_Cup",
    "en_wikipedia_org-wiki-ISMF_World_Cup_Ski_Mountaineering",
    "en_wikipedia_org-wiki-Bobsleigh_World_Cup",
    "en_wikipedia_org-wiki-Luge_World_Cup",
    "en_wikipedia_org-wiki-Skeleton_World_Cup",
    "en_wikipedia_org-wiki-ISU_Speed_Skating_World_Cup",
    "en_wikipedia_org-wiki-ISU_Short_Track_Speed_Skating_World_Cup",
    "en_wikipedia_org-wiki-FIS_Alpine_Ski_World_Cup",
    "en_wikipedia_org-wiki-FIS_Cross-Country_World_Cup",
    "en_wikipedia_org-wiki-FIS_Freestyle_Ski_World_Cup",
    "en_wikipedia_org-wiki-FIS_Ski_Cross_World_Cup",
    "en_wikipedia_org-wiki-FIS_Nordic_Combined_World_Cup",
    "en_wikipedia_org-wiki-FIS_Ski_Jumping_World_Cup",
    "en_wikipedia_org-wiki-FIS_Ski_Flying_World_Cup",
    "en_wikipedia_org-wiki-FIS_Snowboard_World_Cup",
    "en_wikipedia_org-wiki-Finland",
    "en_wikipedia_org-wiki-Commonwealth_of_Independent_States",
    "en_wikipedia_org-wiki-Canada",
    "en_wikipedia_org-wiki-Slovakia",
    "en_wikipedia_org-wiki-Bulgaria",
    "en_wikipedia_org-wiki-Switzerland",
    "en_wikipedia_org-wiki-Czech_Republic",
    "en_wikipedia_org-wiki-Ukraine",
    "en_wikipedia_org-wiki-Norway",
    "en_wikipedia_org-wiki-France",
    "en_wikipedia_org-wiki-East_Germany",
    "en_wikipedia_org-wiki-Germany",
    "en_wikipedia_org-wiki-Soviet_Union",
    "en_wikipedia_org-wiki-West_Germany",
    "en_wikipedia_org-wiki-Russia",
    "en_wikipedia_org-wiki-Sweden",
    "en_wikipedia_org-wiki-Italy",
    "en_wikipedia_org-wiki-China",
    "en_wikipedia_org-wiki-United_States",
    "en_wikipedia_org-wiki-Austria",
    "en_wikipedia_org-wiki-Belarus",
    "en_wikipedia_org-wiki-Poland",
    "en_wikipedia_org-wiki-Czechoslovakia",
    "en_wikipedia_org-wiki-Slovenia",
    "en_wikipedia_org-wiki-Romanization",
    "en_wikipedia_org-wiki-Cyrillic_script",
    "en_wikipedia_org-wiki-List_of_IOC_country_codes",
    "en_wikipedia_org-wiki-BMW",
    "en_wikipedia_org-wiki-Wikipedia:File_Upload_Wizard",
    "en_wikipedia_org-wiki-Category:Articles_with_short_description",
    "en_wikipedia_org-wiki-Category:Short_description_matches_Wikidata",
    "en_wikipedia_org-wiki-Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_4_0_International_License",
    "en_wikipedia_org-wiki-Wikipedia:General_disclaimer",
    "en_wikipedia_org-wiki-Bobsleigh_World_Cup",
    "en_wikipedia_org-wiki-Luge_World_Cup",
    "en_wikipedia_org-wiki-Skeleton_World_Cup",
    "en_wikipedia_org-wiki-ISU_Speed_Skating_World_Cup",
    "en_wikipedia_org-wiki-ISU_Short_Track_Speed_Skating_World_Cup",
    "en_wikipedia_org-wiki-Template:Main_world_championships",
    "en_wikipedia_org-wiki-Help:Category",
    "en_wikipedia_org-wiki-Category:CS1_Norwegian-language_sources_(no)",
    "en_wikipedia_org-wiki-Category:Short_description_is_different_from_Wikidata",
    "en_wikipedia_org-wiki-Category:Articles_containing_Norwegian-language_text",
    "en_wikipedia_org-wiki-Category:Commons_category_link_is_on_Wikidata",
    "en_wikipedia_org-wiki-Category:Articles_with_Russian-language_sources_(ru)",
    "en_wikipedia_org-wiki-Category:Articles_with_Ukrainian-language_sources_(uk)",
    "en_wikipedia_org-wiki-Category:Articles_with_GND_identifiers",
    "en_wikipedia_org-wiki-Category:Articles_with_J9U_identifiers",
    "en_wikipedia_org-wiki-Category:Articles_with_LCCN_identifiers",
    "en_wikipedia_org-wiki-Category:Articles_with_NDL_identifiers",
    "en_wikipedia_org-wiki-Category:Articles_with_NKC_identifiers",
    "en_wikipedia_org-wiki-Category:Racing",
    "en_wikipedia_org-wiki-Category:Snowboarding",
    "en_wikipedia_org-wiki-Help:Authority_control",
    "en_wikipedia_org-wiki-Ski_lift",
    "en_wikipedia_org-wiki-Aerial_tramway",
    "en_wikipedia_org-wiki-Chairlift",
    "en_wikipedia_org-wiki-Detachable_chairlift",
    "en_wikipedia_org-wiki-Funicular",
    "en_wikipedia_org-wiki-Funifor",
    "en_wikipedia_org-wiki-Funitel",
    "en_wikipedia_org-wiki-Gondola_lift",
    "en_wikipedia_org-wiki-Bicable_gondola_lift",
    "en_wikipedia_org-wiki-Tricable_gondola_lift",
    "en_wikipedia_org-wiki-Hybrid_lift",
    "en_wikipedia_org-wiki-Surface_lift",
    "en_wikipedia_org-wiki-Ski_resort",
    "en_wikipedia_org-wiki-Dry_ski_slope",
    "en_wikipedia_org-wiki-Superpipe",
    "en_wikipedia_org-wiki-Piste",
    "en_wikipedia_org-wiki-Paralympic_cross-country_skiing",
    "en_wikipedia_org-wiki-Ski_flying",
    "en_wikipedia_org-wiki-Ski_marathon",
    "en_wikipedia_org-wiki-Ski_orienteering",
    "en_wikipedia_org-wiki-Ski_touring",
    "en_wikipedia_org-wiki-Backcountry_skiing",
    "en_wikipedia_org-wiki-Roller_skiing",
    "en_wikipedia_org-wiki-Skijoring",
    "en_wikipedia_org-wiki-Slalom_skiing",
    "en_wikipedia_org-wiki-Giant_slalom",
    "en_wikipedia_org-wiki-Super-G",
    "en_wikipedia_org-wiki-Downhill_(ski_competition)",
    "en_wikipedia_org-wiki-Alpine_skiing_combined",
    "en_wikipedia_org-wiki-Extreme_skiing",
    "en_wikipedia_org-wiki-Glade_skiing",
    "en_wikipedia_org-wiki-Heliskiing",
    "en_wikipedia_org-wiki-Para-alpine_skiing",
    "en_wikipedia_org-wiki-Speed_skiing",
    "en_wikipedia_org-wiki-Indoor_skiing",
    "en_wikipedia_org-wiki-Night_skiing",
    "en_wikipedia_org-wiki-Modern_competitive_archery",
    "en_wikipedia_org-wiki-Telemark_skiing",
    "en_wikipedia_org-wiki-Aerial_skiing",
    "en_wikipedia_org-wiki-Big_air",
    "en_wikipedia_org-wiki-Freeriding_(sport)",
    "en_wikipedia_org-wiki-Freeskiing",
    "en_wikipedia_org-wiki-Half-pipe_skiing",
    "en_wikipedia_org-wiki-Mogul_skiing",
    "en_wikipedia_org-wiki-Ski_ballet",
    "en_wikipedia_org-wiki-Ski_cross",
    "en_wikipedia_org-wiki-Slopestyle",
    "en_wikipedia_org-wiki-Alpine_snowboarding",
    "en_wikipedia_org-wiki-Backcountry_snowboarding",
    "en_wikipedia_org-wiki-Freestyle_snowboarding",
    "en_wikipedia_org-wiki-Half-pipe",
    "en_wikipedia_org-wiki-Snowboard_cross",
    "en_wikipedia_org-wiki-Snowboard_racing",
    "en_wikipedia_org-wiki-Carved_turn",
    "en_wikipedia_org-wiki-Jump_turn",
    "en_wikipedia_org-wiki-Parallel_turn",
    "en_wikipedia_org-wiki-Pivot_turn_(skiing)",
    "en_wikipedia_org-wiki-Snowplough_turn",
    "en_wikipedia_org-wiki-Stem_christie",
    "en_wikipedia_org-wiki-Ski_school",
    "en_wikipedia_org-wiki-Ski_simulator",
    "en_wikipedia_org-wiki-Ski_binding",
    "en_wikipedia_org-wiki-Ski_boot",
    "en_wikipedia_org-wiki-Ski_helmet",
    "en_wikipedia_org-wiki-Monoski",
    "en_wikipedia_org-wiki-Alpine_skiing",
    "en_wikipedia_org-wiki-Freestyle_skiing",
    "en_wikipedia_org-wiki-Nordic_combined",
    "en_wikipedia_org-wiki-Ski_jumping",
    "en_wikipedia_org-wiki-Snowboarding",
    "en_wikipedia_org-wiki-Ski_mountaineering",
    "en_wikipedia_org-wiki-Bobsleigh",
    "en_wikipedia_org-wiki-Skeleton_(sport)",
    "en_wikipedia_org-wiki-Curling",
    "en_wikipedia_org-wiki-Ice_hockey",
    "en_wikipedia_org-wiki-Luge",
    "en_wikipedia_org-wiki-Ice_skating",
    "en_wikipedia_org-wiki-Figure_skating",
    "en_wikipedia_org-wiki-Short-track_speed_skating",
    "en_wikipedia_org-wiki-Long-track_speed_skating",
    "en_wikipedia_org-wiki-ISBN_(identifier)",
    "en_wikipedia_org-wiki-Special:BookSources-978-1386671152",
    "en_wikipedia_org-wiki-Template:Cite_web",
    "en_wikipedia_org-wiki-Category:CS1_maint:_numeric_names:_authors_list",
    "en_wikipedia_org-wiki-Rounding",
    "en_wikipedia_org-wiki-European_Broadcasting_Union",
    "en_wikipedia_org-wiki-Template:Winter_Olympic_sports",
    "en_wikipedia_org-wiki-Template_talk:Winter_Olympic_sports",
    "en_wikipedia_org-wiki-Special:EditPage-Template:Winter_Olympic_sports",
    "en_wikipedia_org-wiki-File:Olympic_rings_without_rims_svg",
    "en_wikipedia_org-wiki-Das_Erste",
    "en_wikipedia_org-wiki-ZDF",
    "en_wikipedia_org-wiki-ORF_(broadcaster)",
    "en_wikipedia_org-wiki-Norsk_Rikskringkasting",
    "en_wikipedia_org-wiki-L%27%C3%89quipe_(TV_channel)",
    "en_wikipedia_org-wiki-Yleisradio",
    "en_wikipedia_org-wiki-Estonia",
    "en_wikipedia_org-wiki-ETV_(Estonia)",
    "en_wikipedia_org-wiki-Latvia",
    "en_wikipedia_org-wiki-LTV_7",
    "en_wikipedia_org-wiki-Lithuania",
    "en_wikipedia_org-wiki-Lithuanian_National_Radio_and_Television",
    "en_wikipedia_org-wiki-Croatia",
    "en_wikipedia_org-wiki-Hrvatska_radiotelevizija",
    "en_wikipedia_org-wiki-Polsat",
    "en_wikipedia_org-wiki-UA:PBC",
    "en_wikipedia_org-wiki-Sveriges_Television",
    "en_wikipedia_org-wiki-Match_TV",
    "en_wikipedia_org-wiki-Channel_One_Russia",
    "en_wikipedia_org-wiki-RTV_Slovenia",
    "en_wikipedia_org-wiki-Bosnia_and_Herzegovina",
    "en_wikipedia_org-wiki-Radio-televizija_Bosne_i_Hercegovine",
    "en_wikipedia_org-wiki-Bulgarian_National_Television",
    "en_wikipedia_org-wiki-South_Korea",
    "en_wikipedia_org-wiki-Korean_Broadcasting_System",
    "en_wikipedia_org-wiki-Eurosport",
    "en_wikipedia_org-wiki-Sponsor_(commercial)",
    "en_wikipedia_org-wiki-Erdinger",
    "en_wikipedia_org-wiki-Viessmann",
    "en_wikipedia_org-wiki-Deutsche_Kreditbank",
    "en_wikipedia_org-wiki-File:Biathlon_Oberhof_2013-039_jpg",
    "en_wikipedia_org-wiki-File:Ben_Woolley_jpg",
    "en_wikipedia_org-wiki-File:Commons-logo_svg",
    ]

scraped = []

def scrape_links(
    scheme: str,
    origin: str,
    path: str,
    depth = 3,
    sitemap: dict = defaultdict(lambda: ""),
):
    siteUrl = scheme + "://" + origin + path
    cleanedUrl = cleanUrl(siteUrl)
    cleanedOrigin = cleanUrl(origin)
    validOrigin = cleanedOrigin + "-"


    if sitemap[cleanedUrl] != "":
        return

    if cleanedUrl in skip_these:
        return
    
    if depth < 0:
        return

    
    if cleanedUrl.endswith("_pdf"):
        print("*** Skipping PDF: " + cleanedUrl)
        return

    if cleanedUrl.endswith("_jpg"):
        print("*** Skipping JPG: " + cleanedUrl)
        return

    if cleanedUrl.endswith("_svg"):
        print("*** Skipping SVG: " + cleanedUrl)
        return
    
    if cleanedUrl.startswith(cleanedOrigin + "-ru-") or (cleanedUrl.startswith(cleanedOrigin + "-de-")):
        print("*** Skipping ru/de: " + cleanedUrl)
        return

    if cleanedUrl.endswith(cleanedOrigin + "-ru") or (cleanedUrl.endswith(cleanedOrigin + "-de")):
        print("*** Skipping ru/de: " + cleanedUrl)
        return

    if not ((cleanedOrigin in cleanedUrl) and ((validOrigin in cleanedUrl) or (cleanedOrigin == cleanedUrl))):
        print("*** Skipping incorrect URL: " + cleanedUrl)
        return

    print(">>> " + cleanedUrl)
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
# Fix this if dynamic stuff, maybe a file to read from?
# parser.add_argument("--site", type=str, required=True)
parser.add_argument("--depth", type=int, default=3)


if __name__ == "__main__":
    args = parser.parse_args()

    depth = args.depth
    sitemap: dict = defaultdict(lambda: "")

    sitemap = do_scrape("https://www.skidskytte.se/", 5, sitemap)
    sitemap = do_scrape("https://www.biathlonworld.com/", depth, sitemap)

    sitemap = do_scrape("https://en.wikipedia.org/wiki/Biathlon_World_Cup", 0, sitemap)
    sitemap = do_scrape("https://en.wikipedia.org/wiki/Biathlon", 0, sitemap)
    sitemap = do_scrape("https://en.wikipedia.org/wiki/IBU_Summer_Biathlon", 0, sitemap)

    # sitemap = do_scrape("https://en.wikipedia.org/wiki/Cross-country_skiing_(sport)", 1, sitemap)
    # sitemap = do_scrape("https://en.wikipedia.org/wiki/Cross-country_skiing", 1, sitemap)
    # sitemap = do_scrape("https://en.wikipedia.org/wiki/International_Ski_and_Snowboard_Federation", 1, sitemap)
    # sitemap = do_scrape("https://en.wikipedia.org/wiki/Shooting_sports", 1, sitemap)

    with open("./scrape/sitemap.json", "w") as f:
        f.write(json.dumps(sitemap))

    print("*** Dumping keys")
    for key in sitemap.keys():
        print(key)
