OPTION_A = 'a'
OPTION_B = 'b'

class Card():
    def __init__(self, card_info):
        self._card_number = card_info['#']
        self._option_a = self._parse_option_str(card_info["Yea Vote (Op A) Results"])
        self._option_b = self._parse_option_str(card_info["Nay Vote (Op B) Results"])
        
######################## 
### ACCESSOR METHODS ###
######################## 
    def get_option(self,option):
        '''
        Returns the dict containing the roles and point values for a specified card option
        
        Parameters:
        option(constant): Constant value. Either OPTION_A or OPTION_B
        
        Returns: 
        dict: corresponding dictionary of roles and point values for the 
              specified card option
        '''
        if option == OPTION_A:
            return self._option_a
        else: 
            return self._option_b

    def get_card_number(self):
        '''
        Returns the card number of the card
        '''
        return self._card_number

###################### 
### HELPER METHODS ###
###################### 
    def _parse_option_str(self, option_str):
        ''' 
        Parses card option str that has been imported from csv file describing card

        Parameters:
        option_str(str): String representing point values for given roles

        Returns:
        dict: Dictionary of roles with their associated point value
        '''
        option_dict = {}
        formatted_option_str = option_str.lower()
        for role in formatted_option_str.split(','):
            name,points = role.split('+')
            option_dict[name.strip()] = points.strip()
        return option_dict

    def __str__(self):
        '''
        Create formatted string representing card

        Returns:
        str: Formatted string 
        '''
        card_str = "Card Number: {}\n".format(self.card_number)

        card_str = card_str + "Option A\n"
        for role,value in self.card_values[0].items():
            card_str = card_str + "    {}: {}\n".format(role,value)

        card_str = card_str + "Option B\n"
        for role,value in self.card_values[1].items():
            card_str = card_str + "    {}: {}\n".format(role,value)

        return card_str


