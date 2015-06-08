#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
I am a bot that tweets an object from the collection of the Finnish National
Gallery: Ateneum, Kiasma and Sinebrychoff art museums.
"""
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import os
import random
from twitter import *  # pip install twitter
import webbrowser
import yaml  # pip install pyaml
from xml.etree.cElementTree import parse

try:
    import timing
except:
    pass


# Windows cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def timestamp():
    import datetime
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


def download_xml(filename):
    if not os.path.exists(filename):
        print("Download xml")
        import wget  # pip install wget
        # Assumes filename is just filename with has no path:
        url = ("https://github.com/hugovk/finnishnationalgallery/blob/master/"
               + filename + "?raw=true")
        wget.download(url, out=filename)
        print("")


def get_all_artworks(filename):
    """Return selected fields of all artworks in the XML"""

    artworks = []

    print("Parse file")
    tree = parse(filename)
    root = tree.getroot()

    print("Find")

    for child in root:
        artwork = False
        unit = None
        unit_ok = True
        image_ids = []
        title_fi = None
        title_en = None
        title_se = None
        uri = None
        creator = None
        creation_date = None

        # print(child.tag)
        # print(child.attrib)
        # print(child.text)

        for grandchild in child:
            if grandchild.tag == "{http://purl.org/dc/elements/1.1/}type":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.text == "artwork":
                    artwork = True
                elif grandchild.text == "artist":
                    break

            elif grandchild.tag == \
                    "{http://purl.org/dc/elements/1.1/}relation":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.attrib == {'type': 'image'}:
                    image_ids.append(grandchild.text)
                    # print(grandchild.text)

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}title":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.attrib == {'lang': 'fi'}:
                    title_fi = grandchild.text
                elif grandchild.attrib == {'lang': 'en'}:
                    title_en = grandchild.text
                elif grandchild.attrib == {'lang': 'se'}:
                    title_se = grandchild.text

            elif grandchild.tag == \
                    "{http://purl.org/dc/elements/1.1/}identifier":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.attrib == {'type': 'uri'}:
                    uri = grandchild.text

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}date":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.attrib == {'type': 'creation'}:
                    creation_date = grandchild.text

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}creator":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                # if grandchild.attrib == {'type': 'c'}:
                creator = grandchild.text

            if (args.unit):
                if grandchild.tag == \
                        "{http://purl.org/dc/elements/1.1/}publisher":
                    # print(grandchild.tag)
                    # print(grandchild.attrib)
                    # print(grandchild.text)
                    if grandchild.attrib == {'type': 'unit'}:
                        unit = grandchild.text
                        # print(args.unit, unit)
                        if not unit.lower().startswith(args.unit):
                            unit_ok = False

        if artwork and unit_ok:
            if len(image_ids):
                artworks.append([image_ids,
                                 title_fi, title_en, title_se,
                                 creator,
                                 creation_date,
                                 uri
                                 ])

    return artworks


def random_artwork(artworks):
    if len(artworks) == 0:
        return None
    randnum = random.randrange(len(artworks))
    print("Random number: " + str(randnum))
    artwork = artworks[randnum]
    print(artwork)
    return artwork


def link_length(link):
    # https://dev.twitter.com/docs/tco-link-wrapper/faq#How_long_are_t.co_links
    # https://dev.twitter.com/docs/api/1.1/get/help/configuration

    if link.startswith("https:"):
        length = 23
    elif link.startswith("http:"):
        length = 22
    return length


def build_tweet(artwork):
    image_ids, title_fi, title_en, title_se, creator, creation_date, uri = \
        artwork
    tweet = ""

    # Prepare values

    # Just use first image_id

    # http://kokoelmat.fng.fi/app?action=image&iid=A0027200&profile=topicartworkbignew
    # http://kokoelmat.fng.fi/app?action=image&iid=A0027200&profile=selectorthumb

    img_link = ("http://kokoelmat.fng.fi/app?action=image&iid={}&profile="
                "topicartworkbignew#.jpg".format(image_ids[0]))
    print(img_link)

    # Pick a title
    if title_en:
        title = title_en
    elif title_fi:
        title = title_fi
    elif title_se:
        title = title_se
    else:
        title = ""

    if title == "nimetön":
        title = "unnamed"
    print_it(title)

    if creator == "tuntematon":
        creator = "unknown"

    if creator:
        creator = "by " + creator
    else:
        creator = ""

    if creation_date == "ajoittamaton":  # "undated"
        creation_date = ""
    elif creation_date is None:
        creation_date = ""

    # Most creation dates aren't in brackets, but some are.
    # Remove any brackets, then add them.
    if len(creation_date):
        if (creation_date[0] == "(" and creation_date[-1] == ")") or \
           (creation_date[0] == "[" and creation_date[-1] == "]"):
            creation_date = creation_date[1:-1]
        creation_date = "(" + creation_date + ")"

    fng_link = uri + "&lang=en"

    # Built tweet
    # Like this:
    # title by creator (creation_date) FNG_link image_link
    # title (creation_date) FNG_link image_link
    # title by creator FNG_link image_link
    # by creator FNG_link image_link

    # Always space before links

    # Add commas and spaces.
    # Keep title 'clean' in case it's too long and needs trimming.
    if title and creator and creation_date:
        creator = " " + creator + " "
    elif title and not creator and creation_date:
        creation_date = " " + creation_date
    elif title and creator and not creation_date:
        creator = " " + creator

    # Title might be too long, find length of others first.
    # We have 140 chars to use.
    remaining = 140
    remaining -= len(creator)
    remaining -= len(creation_date)
    remaining -= 1  # space before link
    remaining -= link_length(fng_link)
    remaining -= 1  # space before link
    remaining -= link_length(img_link)

    if len(title) > remaining:
        title = title[:remaining - 1] + "…"  # 1: ellipsis

    print_it("T:" + title + ":T")
    print_it("C:" + creator + ":C")
    print_it("D:" + creation_date + ":D")

    tweet = title + creator + creation_date + " " + fng_link + " " + img_link
    print_it(">" + tweet + "<")
    return tweet


def load_yaml(filename):
    if not os.path.exists(filename):
        print("Create " + filename + " with Twitter credentials")

    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {'oauth_token', 'oauth_token_secret',
                               'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials):
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file. See data/onthisday_example.yaml
    t = Twitter(auth=OAuth(credentials['oauth_token'],
                           credentials['oauth_token_secret'],
                           credentials['consumer_key'],
                           credentials['consumer_secret']))

    print_it("TWEETING THIS:\n" + string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        result = t.statuses.update(status=string)
        url = ("http://twitter.com/" + result['user']['screen_name'] +
               "/status/" + result['id_str'])
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


if __name__ == '__main__':
    timestamp()

    parser = argparse.ArgumentParser(
        description="I am a bot that tweets an object from the collection of "
                    "the Finnish National Gallery: Ateneum, Kiasma and "
                    "Sinebrychoff art museums.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        # default='/Users/hugo/Dropbox/bin/data/fngbot.yaml',
        default='M:/bin/data/fngbot.yaml',
        help="YAML file location containing Twitter key and secret")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: don't tweet")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '--xml', default='fng-data-dc.xml',
        help="XML file location containing artwork data")
    parser.add_argument(
        '-u', '--unit',
        choices=['ateneum', 'kiasma', 'sinebrychoff'],
        help="Unit of Finnish National Gallery that houses the artwork. "
             "Either Ateneum, Kiasma or Sinebrychoff Art Museum (SF). "
             "Sinebrychoff Art Museum houses old international art from the "
             "14th century to the early 19th century. The Ateneum Art Museum "
             "houses pre-1960 Finnish art and international art from the "
             "19th and 20th centuries. The Museum of Contemporary Art Kiasma "
             "houses post-1960 Finnish and international art.")
    args = parser.parse_args()
    print(args)

    download_xml(args.xml)
    artworks = get_all_artworks(args.xml)
    print(str(len(artworks)) + " artworks found")

    artwork = random_artwork(artworks)
    if artwork is None:
        import sys
        sys.exit("No artwork found")

    twitter_credentials = load_yaml(args.yaml)

    tweet = build_tweet(artwork)
    print_it("Tweet this:\n" + tweet)
    tweet_it(tweet, twitter_credentials)

# End of file
