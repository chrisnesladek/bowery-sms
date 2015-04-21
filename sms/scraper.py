#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Scrape the daily workouts from Bowery CrossFit blog's sitemap.
URL = 'http://www.bowerycrossfit.com/post-sitemap.xml'

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import requests
import bs4
import re
import unicodedata

from HTMLParser import HTMLParser

from parse_rest.connection import register
from parse_rest.datatypes import Object

# Common abbreviations to help reduce the text message length.
abbreviations = {
    'minutes': 'min',
    'seconds': 'sec',
    'meters': 'm',
    'Chest-to-Bar': 'CTB',
    'Pull-Ups': 'PU',
    'as many rounds and reps as possible': 'AMRAP',
    'as many rounds as possible': 'AMRAP',
    'as many reps as possible': 'AMRAP',
    'back squat': 'BS',
    'hang squat clean': 'HSC',
    'hang clean': 'HC',
    'clean and jerk': 'C&J',
    'every minute on the minute': 'EMOM',
    'front squat': 'FS',
    'hand stand push up': 'HSPU',
    'knees to elbow': 'KTE',
    'muscle ups': 'MU',
    'overhead squat': 'OHS',
    'power clean': 'PC',
    'push press': 'PP',
    'push jerk': 'PJ',
    'power snatch': 'PSN',
    'squat clean': 'SC',
    'sumo deadlift high pull': 'SDHP',
    'toes to bar': 'TTB',
    'push-ups': 'PU',
    'snatch': 'SN',
    'squat': 'SQ',
    'kettlebell': 'KB',
    'clean': 'CLN',
    'deadlift': 'DL',
    ' one': ' 1',
    ' two': ' 2',
    ' three': ' 3',
    ' four': ' 4',
    ' five': ' 5',
    'rounds for time of': 'RFT',
    'rounds for time': 'RFT',
    'alternating': 'alt',
    'sit-ups': 'SU',
    'Sit-Ups': 'SU',
    'Double-Unders': 'DU',
    }

# This is ugly. I should do this better.
# Todo: Actually learn about encoding.
special_chars = {
    '’': "'",
    '‘': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '\xc2\xa0' : ' ',
    }

class Workout(Object):
    pass

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_programming_urls():
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text)

    # reverse to get the most recent urls first
    urls = list(reversed([url.text for url in soup.findAll("loc")]))

    # limit to last 5 urls
    del urls[5:]

    # reverse on return to process in asc order
    return reversed(urls)

def has_wod(content):
    if "Workout:" in content and not "open gym" in content:
        return True
    else:
        return False

def clean_content(content):
    if "Open Workout:" in content:
        clean = re.sub('Recommended content:.*?Open Workout:','', strip_tags(content.replace("</p>", "</p> ")), flags=re.DOTALL)
    else:
        clean = re.sub('Recommended content:.*?Workout:','', strip_tags(content.replace("</p>", "</p> ")), flags=re.DOTALL)
    return clean

def condensed_content(content):
    for key in special_chars:
        content = content.replace(key, special_chars[key])

    content = content.replace('\n \n','')
    content = content.replace('\n ','')
    content = re.sub(' +',' ', content)
    content = content.replace(' :', ':')

    for key in abbreviations:
        content = content.replace(key, abbreviations[key])
        content = content.replace(key.capitalize(), abbreviations[key])

    return content.strip()

def save_workout(slug, raw, condensed):
    print 'Slug: ', slug
    print 'Raw: ', raw

    # split the workout for open and experiencd tracks
    workouts = condensed.split("Experienced Workout:")

    # default to same workout for both tracks
    open_workout = workouts[0]
    experienced_workout = workouts[0]

    # if len == 2, there is an experienced track; assign
    if len(workouts) == 2:
        experienced = workouts[1].replace("Experienced Workout:\n", "")

    print 'Open: ', open_workout
    print 'Experienced: ', experienced_workout

    workout = Workout(slug=slug, raw=raw, open=open_workout, experienced=experienced_workout, sent=False)
    return workout.save()

if __name__ == '__main__':
    register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'])

    # Get most recent blog programming posts
    blog_posts = get_programming_urls()

    # For each blog post...
    for post in blog_posts:
        response = requests.get(post)
        soup = bs4.BeautifulSoup(response.text)

        # Get content for each post
        content = str(soup.select('div.single-post-content')).strip('[]')

        # If the post contains a WOD
        if has_wod(content):

            # Get slug from the URL
            slug = post.replace("http://www.bowerycrossfit.com/programming-", "").strip("/")

            # Does the slug already exist?
            slug_exist = Workout.Query.all().filter(slug=slug).limit(1)

            if slug_exist.count() == 0:
                # If not, save the workout
                raw = clean_content(content)
                condensed = condensed_content(raw)
                save_workout(slug, raw, condensed)
            else:
                print 'No new workouts.'


