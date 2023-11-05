
class Gateway:
    def get_all_possible_words(self):
        word_list = []
        with open('./data/words.txt') as f:
            word_list.extend([word.strip() for word in f.readlines()])
            
        return word_list
