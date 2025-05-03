import random
from Words import words
import string


def get_valid_words(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word


def hangman():
    word = get_valid_words(words)
    word_letters = set(word)
    alphabet = set(string.ascli_uppercase) 
    used_letters = set()

 while_len(word_letters) > 0:
    user_letter = input('Guess a letter: ').upper()
    if user_letter in alphabet - used_letters:
        used_letters.add(used_letters)
        if user_letter in word_letters:
            word_letters.remove(user_letter)
    
    elif user_letter in used_letters:
        print("YOU HAVE ALREADY USED THAT CHARACTER. PLEASE TRY AGAIN")
    
    else:
        print('Invalid Character. please try again')



user_input = input('Type Something')
print(user_input)