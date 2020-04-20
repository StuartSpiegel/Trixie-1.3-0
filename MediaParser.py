# The purpose of this class is define an alternate method for parsing wiki data into an object for processing in
# CommonUtils.py instead of reading from a text file

import argparse

import mwparserfromhell
import pywikibot
import requests
# Global Fields
from mwparserfromhell import wikicode

colorFeatureMap = {}
# Wikicode is a mwparserfromhell.WikiCode object which behaves like a String object with extra methods for encapsulation
# test is the wiki data to parse --> possibly point this to web link
text = '''TWSSAFE-001 [

This is [[SAFe Planning#Program_Increment_4| PI-4]] feature.

==Acceptance Criteria==
* Stickie Template Word Document will be populated from wiki data
* Acceptance Criteria 1
* Acceptance Crtieria 2
** Test 1
** Test 2
==Considerations ==
===Assumptions===
* Wiki data has already been downloaded to hosting machine

===Dependencies===


==Stories (16)==
===Research (2)===
* Research different word document manipulation python libraries (8)

===Software Design & Development (13)===
* Extract data from wiki format (0)
* Populate stickie box title with the feature number (2)
** The box title color should change per feature!
** Another bullet added for test
* Populate each stickie box with the story category (1)
* Populate each stickie box with each story title (3)
* Populate each stickie box with the correct story points (5)

===Testing (1)===
* Develop Unit Test for Trixie Stickies (1)

===Testing (2)===
* Test 
'''

wikicode = mwparserfromhell.parse(text)
print(wikicode)

# Filter the templates
templates = wikicode.filter_templates()
print(templates)

# Get the first element of the parsed data that is in template
element = templates[0]  # Getting the whole template object
print(element.name)
print(element.params)

first = element.get(1).value  # Getting the first list (string) value of the template object
second = element.get(2).value
print(first)  # for testing
print(second)


def getNth_element(index):
    toReturn = element.get(index).value
    return toReturn


# Integration for Trixie Project : If you are not using a library you can use parse() to get any page using the API
# and the requests libraries
# TODO : The integration methods for CommonUtils.py
def parse(title):
    site = pywikibot.Site()
    page = pywikibot.Page(site, title)
    text = page.get()
    return mwparserfromhell.parse(text)


def parseWithParams(title):
    API_URL = "“https://en.wikipedia.org/w/api.php"
    params = {"action:", "query", "prop", "revisions", "rvprop", "content", "rvslots", "main", "rvlimit", "titles",
              "format: json", "formatversion: 2"}
    headers = {"User-Agent": "My -Bot-Name/1.0"}
    req = requests.get(API_URL, headers=headers, params=params)
    res = req.json()
    revision = res["query"]["pages"][0]["revisions"][0]
    textParams = revision["slots"]["main"]["content"]
    return mwparserfromhell.parse(textParams)


# The new definition/version of readInput() will be parse(title) and parseWithParams(title), this method must parse
# all initial arguments and return the storyList and colorFeatureMap
def parseInput(title):
    parser = argparse.ArgumentParser()
    parser.add_argument(title)
    theSite = pywikibot.Site()
    parser.add_argument(theSite)
    thePage = pywikibot.Page(site, title)
    parser.add_argument(thePage)
    site_text = page.get()
    parser.add_argument(site_text)
    storyList = site_text
    return storyList, colorFeatureMap


# Manual testing of the Template filters
# Manual exploration of templates for when WikiCode objects are not contained at the next node to iterate on.
title = " "
site = pywikibot.Site()
page = pywikibot.Page(site, title)
text = page.get()
code = mwparserfromhell.parse(text)
print(code.filter_templates(recursive=False))
temp = code.filter_templates(recursive=False)
# Testing
print(temp.get(1).value)
print(temp.get(1).value.filter_templates()[0])
print(temp.get(1).value.filter_templates()[0].get(1).value)


# Can convert code back into a string object for saving
def toString(text):
    text = str(code)
    print(text)
    text = code


# Build text filters around headings and other iterable fields
def filterSections():
    headings = {}
    comments = {}
    links = {}
    wikiLinks = {}
    filter_text = {}

    for k in wikicode.filter_headings():
        headings += k
    for j in wikicode.filter_comments():
        comments += j
    for n in wikicode.filter_links():
        links += n
    for l in wikicode.filter_wikilinks():
        wikiLinks += l
    for r in wikicode.filter_text():
        filter_text += r


def getArguments():
    arguments = {}
    for j in wikicode.ifilter_arguments():
        arguments += j
        print(arguments)
