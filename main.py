import random
from collections import defaultdict


def secret_santa(people, likes, dislikes, pairs=False):
    # People is a simple list of strings
    # Likes is a dict with the strings from People as keys and a list of strings as items
    # Dislikes is formatted the same way as likes

    # Sort participants by highest number of dislikes first to get them "out of the way".
    # Duplicate People and shuffle list.
    # Go through the shuffled list looking for valid likes. Swap with last place and popright after.

    # Outputs a list of strings, each going "Gifter -> Recepient"
    # "Pairs" is whether a two-person cycle is acceptable or not

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
    chain = {}
    count = 1  # Count number of successful matches. If 0 after a loop, then it's a dead end

    while count != 0 and deck:
        count = 0  # Reset count
        for person in deck:
            searching = True
            index = len(participants)
            while searching and index <= 0:
                index -= 1
                searching = False
                for dislike in dislikes[person]:
                    if searching:
                        break

                    if dislike is None:
                        continue

                    target = participants[index]
                    if target not in dislikes:
                        continue

                    # Check if two person cycle
                    if not pairs and target in chain and chain[target] == person:
                        continue

                    if dislike in likes[target]:
                        searching = True

            # Check if a match was found at all
            if searching:
                temp.append(person)  # Person not found. Add to not working.

            # If reached here, then there are no conflicts
            chain[person] = participants[index]
            count += 1  # Increment found count
            participants[index] = participants[len(participants)]  # Swap with last
            participants.pop()

        # Just went through the entire deck.
        # Replace deck with remainders and empty out the remainder storage.
        deck = temp
        temp = []

    return chain, temp  # Return the secret santa chain and a list of unmatched participants


def pair_valid(likes, dislikes, gifter, recipient):
    for dislike in dislikes[gifter]:
        if dislike is None:
            continue

        if dislike in likes[recipient]:
            return False

    return True


def single_cycle(people, likes, dislikes):
    # Sort participants by highest number of dislikes first to get them "out of the way".
    # Duplicate People and shuffle list.
    # Go through the shuffled list looking for valid likes. Swap with last place and popright after.

    # Outputs a list of names where the person in an index is gifting the next index
    # Also outputs a list of unmatched names

    deck = []
    biggest = cur = -1
    index = -1
    for i, name in enumerate(people):
        count = len(dislikes[name])
        if count > biggest:
            cur = name
            biggest = count
            index = i

    for x in people:
        if index != 0:
            deck.append(x)
        index -= 1
    chain = [cur]
    leftover = []

    while deck:
        gifter = chain[-1]  # Most recent entry is current gifter
        random.shuffle(deck)
        searching = True
        found = -1
        for i, recipient in enumerate(deck):
            if pair_valid(likes, dislikes, gifter, recipient):
                found = i
                break
        if found == -1:
            leftover.append(chain.pop(-1))
            if len(chain) == 0:
                chain = [deck.pop(0)]
        else:
            chain.append(deck.pop(found))

    # Scan for leftovers ONCE
    length = len(chain)-2
    failed = []
    found = False
    for person in leftover:
        print("Finding leftovers for " + person)
        for i in range(length):
            if pair_valid(likes, dislikes, chain[i], person) and pair_valid(likes, dislikes, person, chain[i+1]):
                chain.insert(i+1, person)
                found = True
                break
        if found:
            found = False
        else:
            failed.append(person)

    return chain, failed  # Return the secret santa chain and a list of unmatched participants


if __name__ == '__main__':
    # Dislikes are unweighted. Use None to increase dislike weight for a person.
    names = ['alice', 'john', 'bob']
    wants = {'alice': ['landscape'],
             'john': [],
             'bob': []
             }
    hates = {'alice':[],
             'john': ['landscape'],
             'bob': []
             }
    res = single_cycle(names, wants, hates)
    print(res)
