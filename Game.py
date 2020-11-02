from random import sample, random
from csv import DictReader, DictWriter

class Game: 
    #################
    ### CONSTANTS ###
    #################
    _OPTION_A = "Yea Vote (Op A) Results"
    _OPTION_B = "Nay Vote (Op B) Results" 
    _CARDS_DRAWN_PER_ROUND = 4
    # Output file fields
    _GAME = "game"
    _SCORES = "scores"
    _WINNER = "winner"
    _CARDS_CHOSEN = "cards_chosen"
    
    def __init__(self, filename, rounds, games, weight, output_file, debug_enabled):
        #######################
        ### SETUP VARIABLES ###
        #######################
        self._filename = filename
        self._rounds = rounds
        self._games = games
        self._weight = weight
        self._output_file = output_file
        self._debug_enabled = debug_enabled
        
        if not (0.0 <= self._weight <= 1.0):
            raise self.WeightingError("Weighting must be between 0.0 and 1.0!")
    
        self._total_wins = {}
        
    ##############
    ### ERRORS ###
    ##############
    class WeightingError(Exception):
        '''
        Exception raised for invalid card weighting
        '''

    ######################
    ### HELPER METHODS ###
    ######################
    def _create_deck(self, filename):
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
                    card[self._OPTION_A] = self._format_card_option(card[self._OPTION_A])
                    card[self._OPTION_B] = self._format_card_option(card[self._OPTION_B])
                    deck[int(card['#'])] = card
        return deck

    def _format_card_option(self, option_str):
        '''
        '''
        option_list = []
        for name,points in [role.split('+') for role in option_str.split(',')]:
            option_list.append((name.strip().lower(), points.strip().lower()))
        return option_list
     
    def _print_debug(self, debug_str):
        '''
        '''
        if self._debug_enabled:
            print(debug_str)
            
    #################
    ### ACCESSORS ###
    #################
    def get_filename(self):
        return self._filename
    def get_rounds(self):
        return self._rounds
    def get_games(self):
        return self._games
    def get_weight(self):
        return self._weight
    def get_output_file(self):
        return self._output_file
    def get_total_wins(self):
        return self._total_wins
    
    ###################################
    ### EXTERNAL SIMULATION METHODS ###
    ###################################
    def run_simulation(self):
        '''
        '''
        deck = self._create_deck(self._filename)
        
        with open(self._output_file+".csv", mode='w', newline='') as output_file:
            fieldnames = [self._GAME, self._CARDS_CHOSEN, self._SCORES, self._WINNER]
            output_writer = DictWriter(output_file, fieldnames=fieldnames)
            output_writer.writeheader()

            for game in range(self._games):
                cards_drawn = sample(deck.keys(), self._CARDS_DRAWN_PER_ROUND*self._rounds)
                game_score = {}
                cards_drawn_info = [] # I'm sure there's a better way to save this info
                for card in cards_drawn:
                    option_chosen = self._OPTION_A if random() < self._weight else self._OPTION_B
                    self._print_debug("Card#: {} | Option: {}".format(card, option_chosen))
                    for role,value in deck[card][option_chosen]:
                        game_score[role] = game_score.get(role,0) + int(value)
                        self._print_debug("    {}: {}".format(role, value))
                    cards_drawn_info.append("{} {}".format(card,option_chosen))
                    winner = sorted(game_score,key=game_score.get, reverse=True)[0]
                    
                    self._print_debug("    {}".format(game_score))
                self._total_wins[winner] = self._total_wins.get(winner,0) + 1
                
                # printing the games_score dict as is still had the brackets, which wasn't good for csv
                # this removes the brackets in a probably overly convoluted way
                game_score_str = ','.join("{} {}".format(k,v) for k,v in game_score.items())
                cards_drawn_info_str = ','.join(cards_drawn_info)
                output_writer.writerow({self._GAME: game, self._CARDS_CHOSEN: cards_drawn_info_str, self._SCORES: game_score_str, self._WINNER: winner})
                