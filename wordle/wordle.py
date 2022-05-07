import collections
from itertools import combinations
import requests
import csv
import time
import click

def get_all_possible_words():
    target_url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
    word_list = requests.get(target_url).text.split("\n")
    word_list.sort()
    return word_list


def build_word_matches():
    words = get_all_possible_words()
    start = time.time()
    with open('all_matches.csv', mode='w') as matches:
        writer = csv.writer(matches, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        out = []
        click.echo('preparing')
        click.clear()
        with click.progressbar([combo for combo in combinations(words, 2)], label='Generating word combinations') as combos:
            for (x ,y) in combos:
                match = check_wordle(x,y)
                out.append((x, y, match))
            writer.writerows(out)   
    end = time.time()
    print(end - start)


def load_word_matches():
    with open('all_matches.csv', newline='') as matches:
        start = time.time()
        out = {}
        reader = csv.reader(matches, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in reader:
            w1, w2, match = row
            if not out.get(w1): out[w1] = {}
            out[w1][w2] = match
        
        end = time.time()
        # print(end - start)
    return out


def get_match_for_words(word1, word2, matches):
    try:
        if matches.get(word1) and matches[word1].get(word2):
            return matches[word1][word2]
        elif matches.get(word2) and matches[word2].get(word1):
            return matches[word2][word1]
    except KeyError:
        print(word1, word2)
        raise Exception(f'cant find match for words {word1}, {word2}')


def check_wordle(word, target_word):
    out = [0] * 5
    count = collections.Counter(target_word)
    
    for i in range(5):
        char = word[i]
        if char == target_word[i]:
            count[char] -= 1
            out[i] = 2

    for i in range(5):
        char = word[i]
        if out[i] == 0 and count[char] > 0 and char in target_word:
                count[char] -= 1
                out[i] = 1
    return ''.join(map(str, out))


def get_matches_for_guesses(words, guesses):
    guesses = iter(guesses)
    for guess in guesses:
        match = next(guesses)
        words = [word for word in words if(does_guess_match_word(word, guess, match))]
    return words


def get_matches_for_guess(words, guess, match):
    return [word for word in words if(does_guess_match_word(word, guess, match))]


def does_guess_match_word(word, guess, match):
    count = collections.Counter(word)
    for position, char in enumerate(match):
        if char == '2':
            if word[position] != guess[position]:
                return False
            count[guess[position]] -= 1
            continue
        
        elif char == '1':
            if word[position] == guess[position] or (word[position] != guess[position] and count[guess[position]] == 0):
                return False

            count[guess[position]] -= 1
            continue
            
        if char == '0' and count[guess[position]] > 0:
            return False
    return True



def get_next_best_word_naive(words, matches):
    # start = time.time()
    out = []
    for x in words:
        lengths = []
        for y in words:
            if x == y: continue
            match = get_match_for_words(x, y, matches)
            lengths.append(len(get_matches_for_guess(words, x, match)))    
        mean = sum(lengths)/len(lengths)
        # print(x, mean)
        out.append((x, mean))
            

    out.sort(reverse=True, key=lambda tup: tup[1])
    # end = time.time()
    # print('naive', end - start)
    return out[0:10]

def get_next_best_word_log(words, matches):
    start = time.time()
    lengths = {}    
    for x, y in combinations(words, 2):
        match = get_match_for_words(x, y, matches)
        length = len(get_matches_for_guess(words, x, match))
        if not lengths.get(x): lengths[x] = []
        if not lengths.get(y): lengths[y] = []
        lengths[x].append(length)
        lengths[y].append(length)

    out = [ ( x, sum(lengths[x])/len(lengths[x]))   for x in lengths]
    out.sort(reverse=True, key=lambda tup: tup[1])
    # end = time.time()
    # print('log', end - start)

    return out[0:10]

def get_next_best_word_log_memoed(words, matches):
    # start = time.time()
    lengths = {}
    colours = {}
    
    for x, y in combinations(words, 2):
        match = get_match_for_words(x, y, matches)
        # this only uses match so we could memoise {x[match] = list, y[match] = list}
        length = len(get_memoed_matches_for_guesses(words, x, match, colours))
        if not lengths.get(x): lengths[x] = []
        if not lengths.get(y): lengths[y] = []
        lengths[x].append(length)
        lengths[y].append(length)

    out = [ ( x, sum(lengths[x])/len(lengths[x]))   for x in lengths]
    out.sort(reverse=True, key=lambda tup: tup[1])
    # end = time.time()
    # print('log', end - start)

    return out[0:10]


def get_memoed_matches_for_guesses(words, x, match, memo):
    if not memo.get(x): memo[x] = {}
    if not memo[x].get(match):
        memo[x][match] = get_matches_for_guess(words, x, match)
    
    return memo[x][match]
        