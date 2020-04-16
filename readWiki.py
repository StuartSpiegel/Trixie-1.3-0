# Trixie Version 1.3-0 adding feature to read directly from wiki as opposed to formatted text file
# This Update requires Python 3.4.0 or later

import wikitextparser as wtp
from wikitextparser import WikiLink

# Parsing format for wiki links
# Standard Parsing format for title and text fragments
wl = wtp.parse('[[title#fragment|text]]').wikilinks[0]

# Assign the title of the new wiki link
wl.title = 'new_title'
wl.fragment = 'new_fragment'
wl.text = 'X'

# Implement the SubText parser
WikiLink('[[new_title#new_frgament|X]]')
WikiLink('[[new_title#new_fragment]]')

# Writing the first page template with string formatting
target = "WEB LINK OF TARGET WIKI PAGE"
parsed = wtp.parse(WikiLink(target))
arguments = parsed.templates[0].arguments
parsed.templates[0].arguments[0].value = 'value_1'

# Test the parsing job with a print to console
# Output format : {{ text | value_1 }}
print(parsed)

# Format and print the templates
parsed_new = wtp.parse('{{t1 |b=b|c=c| d={{t2|e=e|f=f}} }}')
t1, t2 = parsed.templates
print(t2.pformat())
print(t1.pformat())

# Cleanup pages using duplicate arguments in template call
t = wtp.Template('{{t|a=a|a=b|a=a}}')
t.rm_dup_args_safe()

# Get the template parameters
params = wtp.parse('{{a|b}}').parameters[0]

# TODO: Get and print the parsed sections with proper formatting
