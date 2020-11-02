from Game import Game
import argparse 

class TheCouncilTextUI:
    def __init__(self):
        args = self._parse_args()
        self._Game = Game(args.filename, args.rounds, args.games, args.weight, args.output_file, args.debug_enabled)
         
    def _parse_args(self):
        '''
        '''
        parser = argparse.ArgumentParser(description="Run game simulation")
        parser.add_argument("filename", help="text file containing card descriptions")
        parser.add_argument("rounds", help="number of rounds", type=int)
        parser.add_argument("games", help="number of games to simulate", type=int)
        parser.add_argument("-weight", "-w", default=.5, help="set weight for option A (which also sets weight for b). value should be between 0.0 and 1.0", type=float)
        parser.add_argument("-output_file", "-of", default="output", help='specify filename for outputted data. default is "output.csv"')
        parser.add_argument("-debug_enabled", "-d", action="store_true")
        return parser.parse_args()
        
    def run_simulation(self):
        '''
        '''
        print("==========================")
        print("THE COUNCIL GAME SIMULATOR")
        print("==========================")
        print("Rounds:{} | Games:{} | Weighting:{}".format(
            self._Game.get_rounds(), self._Game.get_games(), self._Game.get_weight()))
            
        self._Game.run_simulation()
        
        print("\nWinner Tally Across All Games Played")
        print("====================================")
        for role,value in self._Game.get_total_wins().items():
            print("{} {}".format(role.ljust(15),value))
            
if __name__ == "__main__":
    ui = TheCouncilTextUI()
    ui.run_simulation()