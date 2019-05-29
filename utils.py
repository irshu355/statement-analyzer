import re

def hasValue(patterns, text):
   return re.search("(" + ")|(".join(patterns) + ")",text)
