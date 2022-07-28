from collections import defaultdict
from ctypes.wintypes import WORD
from typing import List
import random

WORD_LENGTH = 5
WHITE_SQUARE = '⬜'
YELLOW_SQUARE = '🟨'
GREEN_SQUARE = '🟩'

SQUARES = [
    WHITE_SQUARE,
    YELLOW_SQUARE,
    GREEN_SQUARE,
]

POSSIBLE_WORDS = set()

def getColors(word, guess) -> str:
    wordCharCount = defaultdict(int)
    guessCharCount = defaultdict(int)
    for c in word:
        wordCharCount[c] += 1
    for c in guess:
        guessCharCount[c] += 1

    result = [None] * WORD_LENGTH
    for i, c in enumerate(guess):
        if word[i] == c:
            result[i] = GREEN_SQUARE
        elif c not in word:
            result[i] = WHITE_SQUARE
    
    yellowCount = defaultdict(int)
    for i, c in enumerate(result):
        if c is not None:
            continue
        char = guess[i]
        if yellowCount[char] < wordCharCount[char]:
            result[i] = YELLOW_SQUARE
            yellowCount[char] += 1
        else:
            result[i] = WHITE_SQUARE

    return ''.join(result)

def get_words() -> List[str]:
    words = []
    with open('words_list.txt') as words_file:
        words = [x.strip() for x in words_file.readlines()]
    return words


def main():
    words = get_words()
    wordsCount = len(words)
    POSSIBLE_WORDS = set(words)

    idx = random.randrange(0, wordsCount)
    randomWord = words[idx]

    guesses = []
    for _ in range(WORD_LENGTH):
        while True:
            guess = words[random.randrange(wordsCount)]
            if guess != randomWord:
                guesses.append(guess)
                break
    
    coloredGuesses = []
    for guess in guesses:
        coloredGuesses.append(getColors(randomWord, guess))

    print(f'The word is {randomWord}')
    print(f'The guesses are:')
    for guess in coloredGuesses:
        print(guess)
    print(GREEN_SQUARE * WORD_LENGTH)


    alreadyGuessed = set()
    for guess in coloredGuesses:
        print(f'Try to find a word for guess: {guess}')
        while True:
            userWord = input().strip()
            if len(userWord) != WORD_LENGTH:
                print('Word length must be 5')
                continue
            if userWord not in POSSIBLE_WORDS:
                print('Unknown word')
                continue
            if userWord in alreadyGuessed:
                print('Already guessed')
                continue
            alreadyGuessed.add(userWord)

            colors = getColors(randomWord, userWord)
            correct = colors == guess
            print(f'Your guess is {"correct" if correct else "incorrect"}: {colors}')
            if correct:
                break
    
    print('Congratulations!')

if __name__ == '__main__':
    main()
