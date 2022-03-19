import re
import string
from collections import Counter
from operator import itemgetter

# third party
import requests

def main():
    word_list = get_word_list()
    placed_letters = get_placed_letters()
    good_letters = get_good_letters() + placed_letters
    bad_letters = get_bad_letters()

    print('\n', placed_letters, good_letters, bad_letters, sep='\n')

    suggestions = find_suggestions(word_list, placed_letters, good_letters, bad_letters)

    for word in suggestions:
        print(word)

def find_suggestions(word_list, placed_letters, good_letters, bad_letters):
    suggestions = []
    for word in word_list:
        if check_bad_letters(word, bad_letters) and check_placed_and_good_letters(word, placed_letters, good_letters):
            suggestions.append(word)
    return suggestions


'''
    word (string): any 5 letter word
    placed_letters: list of length 5 of letters
    bad_letters: list of length 5 of letters
    return: True if every letter in word is a placed letter (in the correct spot) or in good_letters, else False
'''
def check_placed_and_good_letters(word, placed_letters, good_letters):
    for i in range(5):
        if placed_letters[i] != '' and word[i] != placed_letters[i]:
            return False
    
    num_good_letters = len(good_letters)
    for i in range(5):
        if placed_letters[i] != '':
            num_good_letters -= 1

    good_letters_in_word = 0
    for i in range(5):
        if word[i] in good_letters:
            good_letters_in_word += 1
    
    if good_letters_in_word >= num_good_letters:
        return True
    else:
        return False

'''
    word (string): any 5 letter word
    bad_letters: list of length 5 of letters
    return: True if no bad letters appear in the given word, else returns False
'''
def check_bad_letters(word, bad_letters):
    for letter in word:
        if letter in bad_letters:
            return False
    return True


def get_word_list():
    print('Fetching word list')
    # get list of five-letter words from meaningpedia.com
    # found it linked from Wikipedia:
    # https://en.wikipedia.org/wiki/Lists_of_English_words#External_links
    meaningpedia_resp = requests.get(
        "https://meaningpedia.com/5-letter-words?show=all")

    # get list of words by grabbing regex captures of response
    # there's probably a far better way to do this by actually parsing the HTML
    # response, but I don't know how to do that, and this gets the job done

    # compile regex
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    # find all matches
    word_list = pattern.findall(meaningpedia_resp.text)
    return word_list

def get_placed_letters():
    placed_letters = []
    print("\nPlaced Letters (blank line means any)")
    for i in range(5):
        letter = input(f"Enter letter {i + 1}: ")
        placed_letters.append(letter.lower())
    return placed_letters

def get_good_letters():
    good_letters = []
    print("\nGood Letters (! when done)")
    while (True):
        letter = input(f"Enter letter: ")
        if letter.lower() == '!':
            break
        else:
            good_letters.append(letter.lower())
    return good_letters

def get_bad_letters():
    bad_letters = []
    print("\nBad Letters (! when done)")
    while (True):
        letter = input(f"Enter letter: ")
        if letter.lower() == '!':
            break
        else:
            bad_letters.append(letter.lower())
    return bad_letters
        

if __name__ == "__main__":
    main()