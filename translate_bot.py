import goslate
import json
import requests
from twython import Twython

# TODO exception 
# TODO length restriction on twitter posts?
# TODO edit dist?
# TODO random choice for subset of all languages?

LANGUAGES = ['ne', 'de']


def get_quote():
    URL = 'http://api.theysaidso.com/qod.json'
    response = requests.get(URL)
    json_dict = json.loads(response.text)
    #length = json_dict['contents']['length']
    #author = json_dict['contents']['author']
    #quote = json_dict['contents']['quote']
    # TODO remove
    quote = "There's such a thin line between winning and losing."
    author = "John R. Tunis" 
    return quote, author

def translate(quote, langs):
    """Translates and reverse-translates the given quote in
    different languages"""
    # the keys in quote_dict are languages
    # the values are pairs containing the quote
    # translated into the destination language and
    # the reverse-translation in the source language
    gs = goslate.Goslate()
    quote_dict = {lang: gs.translate(gs.translate(quote, lang), 'en') for lang in langs}
    return quote_dict

def find_furthest_quote(quote, quote_dict):
    """finds a reverse-translated quote that is most different
    from the original quote"""
    lang = LANGUAGES[0]
    furthest_quote = quote_dict[lang]
    return furthest_quote, lang

def tweet(quote, reverse_quote, lang, author):
    print 'tweet:'
    print '\t', 'en:', quote 
    print '\t', lang, ':', reverse_quote
    print '\t author:', author


def main():
    quote, author = get_quote()
    quote_dict = translate(quote, LANGUAGES)
    print 'quote_dict:', quote_dict
    furthest_quote, lang = find_furthest_quote(quote, quote_dict)
    print 'furthest quote:', furthest_quote
    tweet(quote, furthest_quote, lang, author)
    
            
if __name__ == '__main__':
    main()
