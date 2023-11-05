import collections
from itertools import combinations
import requests
import time
from tqdm import tqdm


BLACK = '0'
YELLOW = '1'
GREEN = '2'


def get_all_possible_words():
    word_list = []
    with open('./data/words.txt') as f:
        word_list.extend([word.strip() for word in f.readlines()])
        
    return word_list


def build_word_matches_naive(words):
    
    # start = time.time()
    out = {}
    
    combos = list(combinations(words, 2))
    with tqdm(combos, desc='Warming up', mininterval=0.3) as combos_progress:
        for (w1 ,w2) in combos_progress:
            match = check_wordle(w1,w2)
            if not out.get(w1): out[w1] = {}
            out[w1][w2] = match
        # end = time.time()
        # print(end - start, len(out))
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
    out = [BLACK] * 5
    count = collections.Counter(target_word)
    
    for i in range(5):
        char = word[i]
        if char == target_word[i]:
            count[char] -= 1
            out[i] = GREEN

    for i in range(5):
        char = word[i]
        if out[i] == BLACK and count[char] > 0 and char in target_word:
                count[char] -= 1
                out[i] = YELLOW
    return ''.join(map(str, out))


def get_matches_for_guesses(words, guesses):
    for guess in guesses:
        words = [word for word in words if(does_guess_match_word(word, guess.word, guess.pattern))]
    return words


def get_matches_for_guess(words, guess, match):
    return [word for word in words if(does_guess_match_word(word, guess, match))]


def does_guess_match_word(word, guess, match):
    count = collections.Counter(word)
    for position, char in enumerate(match):
        if char == GREEN:
            if word[position] != guess[position]:
                return False
            count[guess[position]] -= 1
            continue
        
    for position, char in enumerate(match):
        if char == YELLOW:
            if word[position] == guess[position] or (word[position] != guess[position] and count[guess[position]] == 0):
                return False

            count[guess[position]] -= 1
            continue
            
        if char == BLACK and count[guess[position]] > 0:
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

def get_next_best_word_log_memoed(words, matches, limit):
    lengths = {}
    colours = {}
    # loops through every combination of words.
    # word1 is the potential guess and word 2 is the potential answer.
    # However if the opposite is true we get the same number of options so we dont need to test word2 against word1
    combos = list(combinations(words, 2))
    with tqdm(combos, desc=f'Getting {limit} next best guesses', mininterval=0.3) as combos_progress:
        for word1, word2 in combos_progress:
            match = get_match_for_words(word1, word2, matches)
            length = len(get_memoed_matches_for_guesses(words, word1, match, colours))
            if not lengths.get(word1): lengths[word1] = []
            if not lengths.get(word2): lengths[word2] = []
            lengths[word1].append(length)
            lengths[word2].append(length)

    out = [ ( word, sum(lengths[word])/len(lengths[word]))   for word in lengths]
    out.sort(reverse=True, key=lambda tup: tup[1])

    return out[0:limit]


def get_memoed_matches_for_guesses(words, guess, match, memo):
    if not memo.get(guess): memo[guess] = {}
    if not memo[guess].get(match):
        memo[guess][match] = get_matches_for_guess(words, guess, match)
    
    return memo[guess][match]
        