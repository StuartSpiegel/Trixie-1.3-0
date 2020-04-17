# The purpose of this class is define an alternate method for parsing wiki data into an object for processing in
# CreateStickies.py instead of reading from a text file

import mwparserfromhell
import pywikibot
import requests

# Wikicode is a mwparserfromhell.WikiCode object which behaves like a String object with extra methods for encapsulation
# test is the wiki data to parse --> possibly point this to web link
text = " "
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
# TODO : The integration methods for CreateStickies
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
    text = revision["slots"]["main"]["content"]
    return mwparserfromhell.parse(text)


# Manual exploration of templates for when WikiCode objects are not contained at the next node to iterate on.
text = " "
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
