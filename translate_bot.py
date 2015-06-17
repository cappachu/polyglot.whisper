import goslate
import json
import requests
import random
import operator
import editdistance 
from sets import Set
from twython import Twython

# TODO exception 
# TODO length restriction on twitter posts?
# TODO edit dist?
# TODO random choice for subset of all languages or use all langs
# TODO use of color in languages, connotations


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

def translate(quote):
    """Translates and reverse-translates the given quote in
    different languages"""
    # the keys in quote_dict are languages
    # the values are pairs containing the quote
    # translated into the destination language and
    # the reverse-translation in the source language
    # TODO remove source lang 'en'
    # TODO use source and target lang?
    gs = goslate.Goslate()
    all_langs = gs.get_languages().keys()

    num_langs = 10 #len(all_langs)
    assert(len(all_langs) >= num_langs)
    lang_indices = random.sample(xrange(len(all_langs)), num_langs)
    quote_dict = {all_langs[lang_index]: gs.translate(gs.translate(quote, all_langs[lang_index]), 'en') for lang_index in lang_indices}
    
    return quote_dict

def symmetric_word_dist(quote_one, quote_two):
    words_one = Set(quote_one.split())
    words_two = Set(quote_two.split())
    symmetric_diff = words_one ^ words_two
    return len(symmetric_diff)

def find_furthest_quote(quote, quote_dict):
    """finds a reverse-translated quote that is most different
    from the original quote"""
    # edit distance
    #furthest_quote = max(quote_dict.iteritems(), key=lambda qtuple: editdistance.eval(qtuple[1], quote))
    # symmetric difference of words
    furthest_quote = max(quote_dict.iteritems(), key=lambda qtuple: symmetric_word_dist(qtuple[1], quote))
    return furthest_quote

def tweet(quote, reverse_quote, lang, author):
    print 'tweet:'
    print '\t', 'en:', quote 
    print '\t', lang, ':', reverse_quote
    print '\t author:', author


def main():
    quote, author = get_quote()
    quote_dict = translate(quote)
    lang, furthest_quote = find_furthest_quote(quote, quote_dict)
    tweet(quote, furthest_quote, lang, author)
    
            
if __name__ == '__main__':
    main()
