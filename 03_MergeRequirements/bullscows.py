import random
import argparse
import os.path
import urllib.request
from cowsay import cowsay, get_random_cow, read_dot_cow
from io import StringIO

def bullscows(guess: str, secret: str) -> (int, int):
    guess_set = set(guess)
    secret_set = set(secret)
    cows = len(guess_set.intersection(secret_set))
    bulls = 0
    length = min((len(guess), len(secret)))
    for i in range(length):
        if guess[i] == secret[i]:
            bulls += 1
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    attempts = 0
    guess = ""

    while (guess != secret):
        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки {}, Коровы {}", bulls, cows)

    return attempts

custom_cow = read_dot_cow(StringIO("""
$the_cow = <<EOC;

            $thoughts
            $thoughts
    _  _
    _ _      (0)(0)-._  _.-'^^'^^'^^'^^'^^'--.
    (.(.)----'`        ^^'                /^   ^^-._
    (    `                 \             |    _    ^^-._
    VvvvvvvVv~~`__,/.._>  /:/:/:/:/:/:/:/\  (_..,______^^-.
     `^^^^^^^^`/  /   /  /`^^^^^^^^^>^^>^`>  >        _`)  )
              (((`   (((`          (((`  (((`  

EOC
"""))

def cowsay_print(message):
	print(cowsay(message.strip(), cowfile=custom_cow))

def ask(prompt: str, valid: list[str] = None) -> str:
    cowsay_print(prompt)
    guess = input()
    if valid == None:
        while len(guess) != args.length:
            cowsay_print(prompt)
            guess = input()
    else:
        while not guess in valid:
            cowsay_print(prompt)
            guess = input()
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    cowsay_print(format_string.format(bulls, cows))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('dictionary', action='store', type=str,
                        help='URL или путь к словарю')
    parser.add_argument('length', action='store', default=5, type=int,
                        help='Длина слов в словаре')

    args = parser.parse_args()

    dict = []
    if os.path.exists(args.dictionary):
        with open(args.dictionary, 'r') as f:
            for line in f.readlines():
                word = line.strip()
                if len(word) == args.length:
                    dict.append(word)
    else:
        with urllib.request.urlopen(args.dictionary) as f:
            for line in f.readlines():
                word = line.decode('utf-8').strip()
                if len(word) == args.length:
                    dict.append(word)

    if len(dict) == 0:
        print("Похоже в словаре нет слов заданной длины, попробуйте изменить длину или словарь")
    else:
        attempts_count = gameplay(ask, inform, dict)
        print(f"Поздравляем, вы угадали слово за {attempts_count} попыток!")
