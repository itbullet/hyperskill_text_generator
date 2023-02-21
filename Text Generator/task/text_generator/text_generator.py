from nltk.tokenize import WhitespaceTokenizer
from nltk.probability import FreqDist
from nltk.util import bigrams
from collections import Counter
import random


def text_analyzer(file_data, mode):

    wt = WhitespaceTokenizer()
    tokens_list = wt.tokenize(file_data)

    temp_list = tokens_list
    bigrams_list = list(bigrams(tokens_list))

    markov_chain_temp_dict = Counter(bigrams_list)
    markov_chain_dict = {}

    for key, val in markov_chain_temp_dict.items():
        markov_chain_dict.setdefault(key[0], {}).setdefault(key[1], val)

    if mode == "tokens":

        print("Corpus statistics")
        print(f"All tokens: {FreqDist(tokens_list).N()}")
        print(f"Unique tokens: {FreqDist(tokens_list).B()}")

    elif mode == "bi-gram":

        temp_list = bigrams_list
        print(f"Number of bigrams: {len(bigrams_list)}")

    elif mode == "random_text":

        for i in range(10):

            sentence = []

            while True:
                head_word = str(random.choice(tokens_list))
                if head_word[0].isupper() and head_word[-1] not in [".", "!", "?"]:
                    sentence.append(head_word)
                    break

            while True:
                tail_word = random.choices(list(markov_chain_dict.get(head_word).keys()),
                                           list(markov_chain_dict.get(head_word).values()), k=1)[0]

                if (tail_word[-1] not in [".", "!", "?"]) and len(sentence) < 5:

                    sentence.append(tail_word)
                    head_word = tail_word

                elif len(sentence) > 4:

                    sentence.append(tail_word)

                    if sentence[-1][-1] in [".", "!", "?"]:
                        break

                    head_word = tail_word

            print(*sentence)
        quit()

    answer = ""

    while answer != "exit":
        answer = input()

        if answer == "exit":
            break

        try:

            if mode == "token":
                print(temp_list[int(answer)])

            elif mode == "bi-gram":
                print(f"Head: {temp_list[int(answer)][0]}\t Tail: {temp_list[int(answer)][1]}")

            elif mode == "markov_chain":
                if markov_chain_dict[answer]:
                    print(f"Head: {answer}")
                    for key, val in markov_chain_dict.get(answer).items():
                        print(f"Tail: {key}\tCount: {val}")

        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
        except ValueError:
            print("Value Error. Please input an integer.")
        except TypeError:
            print("Type Error. Please input an integer.")
        except KeyError:
            print("Key Error. The requested word is not in the model. Please input another word.")


def main():

    filename = input()
    with open(filename, "r", encoding="utf-8") as file:
        file_data = file.read()

    text_analyzer(file_data, "random_text")


if __name__ == "__main__":
    main()
