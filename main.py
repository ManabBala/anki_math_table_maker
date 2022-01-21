import requests

parent_number = 0
multiplier_number = 1
max_multiplier_number = 10
tags = ["math_table"]

# input a number
while True:
    try:
        parent_number = int(input("Select Parent Number of your Math Table: "))
        break
    except ValueError:
        print("Please input integer only...")
        continue
print("Selected Number: ", parent_number)

while True:
    include_one = input("Should include '{} x 1 = ?' and '{} x 10 = ?' in the Table(y/n): ".format(parent_number,
                                                                                                   parent_number))
    if include_one == "y":
        break
    elif include_one == "n":
        multiplier_number = 2
        max_multiplier_number = 9
        break
    else:
        continue

deck_name = "Math-Table::{}x({}-{})".format(parent_number, multiplier_number, max_multiplier_number)


# sending cards to the desired deck
def anki_card_push(front, back, i):
    r = requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": tags
            }
        }
    })
    print("Add card status[{}]: {}".format(i, r.json()))


# creating new anki deck if not present
def create_anki_deck(deck):
    print("Deck Name: {}".format(deck))
    r = requests.post('http://127.0.0.1:8765', json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck
        }
    })
    print("Deck create status: {}".format(r.json()))


def make_math_table():
    global multiplier_number
    create_anki_deck(deck_name)
    while multiplier_number <= max_multiplier_number:
        multiplication_value = int(parent_number) * int(multiplier_number)
        anki_front = "{} x {} = ?".format(multiplier_number, parent_number)
        anki_back = "{}".format(multiplication_value)
        anki_card_push(anki_front, anki_back, multiplier_number)
        multiplier_number = multiplier_number + 1
        print(anki_front)
        print(anki_back)


make_math_table()
