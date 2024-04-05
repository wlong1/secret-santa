import random


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


if __name__ == '__main__':
    # Dislikes are unweighted. Use None to increase dislike weight for a person.
    names = []
    wants = {}
    hates = {}
    res = secret_santa(names, wants, hates)
    print(res)
