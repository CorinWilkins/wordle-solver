import collections


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
            if word[position] == guess[position] or (word[position] != guess[position] and count[guess[position]] is 0):
                return False

            count[guess[position]] -= 1
            continue
            
        if char == '0' and count[guess[position]] > 0:
            return False
    return True