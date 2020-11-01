from random import sample, random
import argparse 
from csv import DictReader, DictWriter
#from Card import Card, OPTION_A, OPTION_B

OPTION_A = "Yea Vote (Op A) Results"
OPTION_B = "Nay Vote (Op B) Results" 
CARDS_DRAWN_PER_ROUND = 4
# Output file fields
GAME = "game"
SCORES = "scores"
WINNER = "winner"
CARDS_CHOSEN = "cards_chosen"

            
def create_deck(filename):
    '''
    Create the deck based on a csv file containing card descriptions. 
    
    Parameters
    filename(str): name of .csv file where cards are listed

    Returns:
    dict: dictionary of cards. {card number: Card object}
    '''
    deck = {}
    with open(filename) as csv_file:
        dict_reader = DictReader(csv_file)
        for card in dict_reader:
            if card['#'] != '': #Skip empty lines
                card[OPTION_A] = _format_card_option(card[OPTION_A])
                card[OPTION_B] = _format_card_option(card[OPTION_B])
                deck[int(card['#'])] = card
    return deck

def _format_card_option(option_str):
    '''
    '''
    option_list = []
    for name,points in [role.split('+') for role in option_str.split(',')]:
        option_list.append((name.strip().lower(), points.strip().lower()))
    return option_list

if __name__ == "__main__":
    total_wins = {}

    parser = argparse.ArgumentParser(description="Run game simulation")
    parser.add_argument("filename", help="text file containing card descriptions")
    parser.add_argument("rounds", help="number of rounds", type=int)
    parser.add_argument("games", help="number of games to simulate", type=int)
    parser.add_argument("-weight", "-w", default=.5, help="set weight for option A (which also sets weight for b). value should be between 0.0 and 1.0", type=float)
    parser.add_argument("-output_file", "-of", default="output", help='specify filename for outputted data. default is "output.csv"')
    args = parser.parse_args()

    if not (0.0 <= args.weight <= 1.0):
        raise Exception("Weighting must be between 0.0 and 1.0!")

    print("==========================")
    print("THE COUNCIL GAME SIMULATOR")
    print("==========================")
    print("Rounds:{} | Games:{} | Weighting:{}".format(
        args.rounds, args.games, args.weight))

    total_wins = {}
    deck = create_deck(args.filename)

    with open(args.output_file+".csv", mode='w', newline='') as output_file:
        fieldnames = [GAME, CARDS_CHOSEN, SCORES, WINNER]
        output_writer = DictWriter(output_file, fieldnames=fieldnames)
        output_writer.writeheader()

        for game in range(args.games):
            cards_drawn = sample(deck.keys(), CARDS_DRAWN_PER_ROUND*args.rounds)
            game_score = {}
            cards_drawn_info = [] # I'm sure there's a better way to save this info
            for card in cards_drawn:
                option_chosen = OPTION_A if random() < args.weight else OPTION_B
                for role,value in deck[card][option_chosen]:
                    game_score[role] = game_score.get(role,0) + int(value)
                cards_drawn_info.append("{} {}".format(card,option_chosen))
                winner = sorted(game_score,key=game_score.get, reverse=True)[0]
            total_wins[winner] = total_wins.get(winner,0) + 1

            # printing the games_score dict as is still had the brackets, which wasn't good for csv
            # this removes the brackets in a probably overly convoluted way
            game_score_str = ','.join("{} {}".format(k,v) for k,v in game_score.items())
            cards_drawn_info_str = ','.join(cards_drawn_info)
            output_writer.writerow({GAME: game, CARDS_CHOSEN: cards_drawn_info_str, SCORES: game_score_str, WINNER: winner})

    print("\nWinner Tally Across All Games Played")
    print("====================================")
    for role,value in total_wins.items():
        print("{} {}".format(role.ljust(15),value))
