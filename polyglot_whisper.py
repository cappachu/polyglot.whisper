import goslate
import json
import requests
import random
import argparse
from twython import Twython, TwythonError

NUM_WHISPERS = 10


def whisper(quote, num_people):
    """whisper quote to several people who speak different languages.
    Translates the quote from English to several languages before translating
    back to English"""
    gs = goslate.Goslate()
    all_langs = gs.get_languages()
    all_lang_codes = all_langs.keys()
    assert(len(all_lang_codes) >= num_people)
    lang_indices = random.sample(xrange(len(all_lang_codes)), num_people)
    language_path = ['English']
    new_quote = quote
    for lang_index in lang_indices:
        lang_code = all_lang_codes[lang_index]
        new_quote = gs.translate(new_quote, lang_code)
        language_path.append(all_langs[lang_code])
    # translate back to english
    new_quote = gs.translate(new_quote, 'en')
    language_path.append('English')
    return new_quote, language_path


def tweet_whisper(quote, new_quote, author, language_path, twitter_keys):
    """Tweet the quote. Expects twitter_keys to be a list consisting of: 
        (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)"""
    APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = twitter_keys

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    try:        
        status = '\n'.join([quote, new_quote])
        twitter.update_status(status=status)
    except TwythonError as e:
        print e


def get_quote():
    """Get a quote from theysaidso.com"""
    URL = 'http://api.theysaidso.com/qod.json'
    response = requests.get(URL)
    json_dict = json.loads(response.text)
    #length = json_dict['contents']['length']
    #author = json_dict['contents']['author']
    #quote = json_dict['contents']['quote']
    # TODO find a free quotes repo 
    quote = "There's such a thin line between winning and losing."
    author = "John R. Tunis" 
    return quote, author


def print_whisper(quote, new_quote, author, language_path):
    print '\n'
    print "%s - %s" % (quote, author)
    print language_path[0],
    for lang in language_path[1:]:
        print "-> %s" % (lang),
    print "\n%s - %s" % (new_quote, 'Polyglot Whisper')
    print '\n'



def main():
    parser = argparse.ArgumentParser(description='Polyglot Whispers')
    parser.add_argument('twitter_keys', nargs=4, metavar=('APP_KEY', 'APP_SECRET', 'OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET'), help='APP_KEY APP_SECRET OAUTH_TOKEN OAUTH_TOKEN_SECRET')
    parser.add_argument('--numwhispers', help='number of whispers before converting back to English')
    args = vars(parser.parse_args())

    if not args['twitter_keys']:
        parser.print_help()
        return
    twitter_keys = args['twitter_keys']
    num_whispers = args['numwhispers'] or NUM_WHISPERS
    
    quote, author = get_quote()
    new_quote, language_path = whisper(quote, num_whispers)
    tweet_whisper(quote, new_quote, author, language_path, twitter_keys)
    print_whisper(quote, new_quote, author, language_path)

            
if __name__ == '__main__':
    # TODO handle length restriction (translation api, twitter posts)?
    # TODO handle exceptions (requests, twitter, quote website)
    # TODO use of color in languages, connotations
    main()
