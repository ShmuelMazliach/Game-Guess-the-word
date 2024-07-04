import json
import random
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Guess the Word Game")
    parser.add_argument("file", type=str, help="Path to the JSON file with words")
    parser.add_argument("players", type=int, help="Number of players")
    parser.add_argument("words", type=int, help="Number of words to play with")
    return parser.parse_args()

def load_words(file_path):
    with open(file_path, "r") as file:
        words = json.load(file)
    return list(words.keys()), words

def get_players(num_players):
    return [input(f"Please enter name for player {i + 1}: ") for i in range(num_players)]

def choose_word(word_bank, words):
    word = word_bank.pop(0)
    return word, words[word]

def display_word(secret_word, list_of_guesses, list_of_incorrect_guesses, list_of_players, scores_of_players):
    print("\nIncorrect guesses:", list_of_incorrect_guesses)
    for player, score in zip(list_of_players, scores_of_players):
        print(f"{player}: {score}")
    print("Word: ", end="")
    for letter in secret_word:
        if letter in list_of_guesses:
            print(letter, end="")
        else:
            print("_", end="")
    print()

def main():
    args = parse_arguments()
    word_bank, words = load_words(args.file)
    
    if args.words > len(word_bank):
        print(f"You have only {len(word_bank)} words available.")
        return
    
    word_bank = random.sample(word_bank, args.words)
    list_of_players = get_players(args.players)
    scores_of_players = [0] * args.players

    list_of_guesses = []
    list_of_incorrect_guesses = []

    def choose_word():
        nonlocal list_of_guesses, list_of_incorrect_guesses
        list_of_guesses = []
        list_of_incorrect_guesses = []
        return word_bank.pop(0)

    def display_word(secret_word):
        print("\nIncorrect guesses:", list_of_incorrect_guesses)
        for player, score in zip(list_of_players, scores_of_players):
            print(f"{player}: {score}")
        for letter in secret_word:
            if letter in list_of_guesses:
                print(letter, end="")
            else:
                print("_", end="")
        print()

    while word_bank:
        secret_word = choose_word()
        print(f"Category: {words[secret_word]}")
        count = 0
        while True:
            display_word(secret_word)
            current_player = list_of_players[count]
            guess = input(f"{current_player}, guess a letter: ").lower()
            while guess in list_of_guesses or guess in list_of_incorrect_guesses or len(guess) != 1:
                guess = input(f"{current_player}, guess a letter: ").lower()

            if guess in secret_word:
                list_of_guesses.append(guess)
                scores_of_players[count] += secret_word.count(guess)
            else:
                list_of_incorrect_guesses.append(guess)

            count = (count + 1) % len(list_of_players)

            if all(letter in list_of_guesses for letter in secret_word):
                print(f"The word was: {secret_word}")
                break

        if not word_bank:
            print("The game is over.")
            winner = list_of_players[scores_of_players.index(max(scores_of_players))]
            print(f"The winner is {winner} with {max(scores_of_players)} points!")
            break

if __name__ == 'main':
    main()
    