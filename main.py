import random


def secret_santa(people, likes, dislikes):
    # People is a simple list of strings
    # Likes is a dict with the strings from People as keys and a list of strings as items
    # Dislikes is formatted the same way as likes

    # Sort participants by highest number of dislikes first to get them "out of the way".
    # Duplicate People and shuffle list.
    # Go through the shuffled list looking for valid likes. Swap with last place and popright after.

    # Outputs a list of strings, each going "Gifter -> Recepient"

    deck = []
    temp = []  # Need a temporary list to hold tuples of (# of Dislikes, Person) pairs.
    for name in dislikes:
        count = len(dislikes[name])
        temp.append((count, name))
    temp.sort()
    for x in temp:
        deck.append(x[1])  # Fill deck from max dislikes to least

    participants = random.sample(people, len(people))
    temp = []  # Reset temp. Use it to store leftover and skipped.
    chain = []
    count = 0  # Count number of successful matches. If 0 after a loop, then it's a dead end






    return chain, temp  # Return the secret santa chain and a list of unmatched participants



if __name__ == '__main__':
    # Dislikes are unweighted. Use None to increase dislike weight for a person.
    secret_santa()

