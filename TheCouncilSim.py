from random import sample, choice
import argparse 
from Card import Card
from csv import DictReader 

            
def create_deck(filename):
    '''
    Create the deck based on a csv file containing card descriptions. 
    
    Parameters
    filename(str): name of .csv file where cards are listed

    Returns:
    dict: dictionary of cards. {card number: Card object}
    '''
    deck = {}
    with open(filename) as card_list:
        reader = DictReader(card_list)
        for card in reader:
            if card['#'] != '': #Skip empty lines
                deck[card['#']] = Card(card)
    return deck

if __name__ == "__main__":
    OPTIONS = ['a','b']
    total_wins = {}

    parser = argparse.ArgumentParser(description="Run game simulation")
    parser.add_argument("filename", help="text file containing card descriptions")
    parser.add_argument("players", help="number of players", type=int)
    parser.add_argument("rounds", help="number of rounds", type=int)
    parser.add_argument("games", help="number of games to simulate", type=int)
    args = parser.parse_args()

    deck = create_deck(args.filename)

    cards_drawn = sample(range(1,len(deck)+1),args.players*args.rounds)
    for game in range(args.games):
        game_scores = {}
        for card in cards_drawn:
            card += 2
            option_chosen = choice(OPTIONS)
            option_dict = deck[str(card)].get_option(option_chosen)
            #print("Card: {} Option: {}".format(card,option_chosen))
            for role,value in option_dict.items():
                game_scores[role] = game_scores.get(role,0) + int(value)
        print("Game: {}".format(game))
        print(game_scores)
        winner = sorted(game_scores,key=game_scores.get, reverse=True)[0]
        total_wins[winner] = total_wins.get(winner,0) + 1
    print("Total wins")
    print(total_wins)




    







