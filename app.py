#!/usr/bin/python3
import sys
import datetime
import json
import logging
# logging.basicConfig(level=logging.INFO)
from argparse import ArgumentParser
from nlpre import titlecaps, dedash, identify_parenthetical_phrases
from nlpre import replace_acronyms, replace_from_dictionary
from nlpre import separated_parenthesis, unidecoder, token_replacement
from nlpre import url_replacement, separate_reference

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument(
      "-t", "--text", dest="text", help="The text to clean", metavar="TEXT")
  args = parser.parse_args()
  data = args.text or ''

  ABBR = identify_parenthetical_phrases()(data)
  parsers = [
      dedash(),
      # titlecaps(),
      separate_reference(),
      unidecoder(),
      token_replacement(),
      url_replacement(),
      replace_acronyms(ABBR, underscore=False),
      separated_parenthesis(),
      # replace_from_dictionary(prefix="MeSH_")
  ]

  cleansed = data
  for f in parsers:
    cleansed = f(cleansed)

  sys.stdout.write(cleansed.replace('\n', ' '))