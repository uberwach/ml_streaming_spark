# -*- coding: utf-8 -*-
import requests
from lxml import html
from bs4 import BeautifulSoup


def try_parse_div(div):
    paragraph = div.find("p")

    if paragraph is None:
        return None

    return paragraph.text


def parse_profile(profile_name):
    URL = "https://twitter.com/%s" % profile_name
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")

    divs = soup.findAll("div", class_="js-tweet-text-container")
    parsed_divs = [try_parse_div(div) for div in divs]
    parsed_tweets = [{"user": profile_name, "msg": msg}
                     for msg in parsed_divs
                     if msg is not None]

    return parsed_tweets


if __name__ == "__main__":
    print(repr(parse_profile("Deutscher_17")))
