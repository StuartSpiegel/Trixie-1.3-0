# Trixie Version 1.3-0 adding feature to read directly from wiki as opposed to formatted text file
# **This Update requires Python 3.4.0 or later**
# Either store the parsed wiki data as a template for operations or possibly a wrapper , trying to avoid
# writing/saving files

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
# TODO: Fix target link encapsulation
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
parsed_sections = wtp.parse("""
... == h2 ==
... t2
... === h3 ===
... t3
... === h3 ===
... t3
... == h22 ==
... t22
... {{text|value3}}
... [[Z|X]]
... """)
print(parsed)
# Strip the title line
del parsed.sections[1].title

# Getting list and table data from a wiki format
p = wtp.parse("""{|
... |  Orange    ||   Apple   ||   more
... |-
... |   Bread    ||   Pie     ||   more
... |-
... |   Butter   || Ice cream ||  and more
... |}""")

table_data = p.tables[0].data()
# The default setting is arrangement according to column span and row span attrib
table_data_NOSPAN = p.tables[0].data(span=False)

# Get the list data and sub-list data
list = {"list item 1", "list item 2", "list item 3"}
parsed_list = wtp.parse(list)

wikilist = parsed.get_lists()[0]
print(wikilist.items)

sublists = wikilist.sublists(1)[0].items
print(wikilist.sublists(1)[0].items)

# HTML Tags
ref, references = p.get_tags()
ref.name = "X_NAME"

# Getting parent and child node data | searching for ancestors of a given type
template_1 = wtp.parse("{{a|{{b|{{c|{{d}}}}}}}}").templates[3]
template_ancestors = template_1.ancestors()
template_parents = template_1.parent()

