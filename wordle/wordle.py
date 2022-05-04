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


def get_matches(words, word, match):
    return [guess for guess in words if(does_guess_match_word(guess, word, match))]

def does_guess_match_word(guess, word, match):
    count = collections.Counter(guess)
    for position, char in enumerate(match):
        if char == '2':
            if guess[position] != word[position]:
                return False
            count[word[position]] -= 1
            continue
          
        elif char == '1':
            if guess[position] == word[position] or (guess[position] != word[position] and count[word[position]] is 0):
                return False

            count[word[position]] -= 1
            continue
            
        if char == '0' and count[word[position]] > 0:
            return False
    return True