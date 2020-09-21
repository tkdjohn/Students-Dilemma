import Settings 
class Human_Player(object):
    '''Represents a human player.'''

    @property
    def Bonus(self):
        return(self._bonus)

    @property
    def Score(self):
        return(self._score)

    @property
    def Most_Recent_Choice(self):
        return(self._most_recent_choice)

    def Set_Bonus(self, value):
        self._bonus = value
        preamble = "The voice says, 'A full written confession, which proves your classmate's guilt, "\
            "praises the wisdom of your mentors, extolls the virtues of this wonderful program, and "\
            "includes a commitment to become a mentor after graduation."
        if (value <= 0):
            self.Report(f"{preamble} Flattery and bribery again?! The only thing worse"\
                         " than a cheater is a greedy cheater.'")
        else:
            self.Report(f"{preamble} A most excellent choice.'")

    def Choose(self):
        choices_string = ''
        choices_left = len(Settings.Choices)
        for choice in Settings.Choices:
            choices_left -= 1
            choices_string += f' {choice} ({choice.value})'
            if (choices_left > 0):
                choices_string  += ' or'
 
        choice = self.Prompt('You are seated in a dark room with a bright light shining in your face. A mentor looms over you, looking stern. ' \
            "The mentor's mouth does not move, yet you hear a commanding voice say, 'Your classmate has already been interrogated. " \
            f"Do you{choices_string}? ").lower()

        self._most_recent_choice, trigger_bonus = self.__validate_choice_(choice)
        return trigger_bonus

    def Update_Results(self, round_score, opponent_round_score, opponent_choice):
        self.__opponent_score_ += opponent_round_score
        self._score += round_score

        self.Report(f'You chose to {self._most_recent_choice} for {round_score} points.')
        self.Report(f'Your classmate chose to {opponent_choice} for {opponent_round_score} points.')
        self.Report(f'=========== Scores ===========')
        self.Report(f'          You: {self._score}') 
        self.Report(f'Your Opponent: {self.__opponent_score_}') 
        self.Report('')

    def End_Game(self):
        win_lose = "You failed to outwit the computer!"
        if self._score > self.__opponent_score_:
            win_lose = "Congratulations, you outsmarted the computer!"
        self.Report('=========== GAME OVER ===========')
        self.Report ('          You: {: >3d}'.format(self._score)) 
        self.Report ('Your Opponent: {: >3d}'.format(self.__opponent_score_))
        self.Report (win_lose)
        self.Report ('=========== GAME OVER ===========')

    def Report(self, text):
        print(text)

    def Prompt(self, prompt):
        return input(prompt)

    def __init__(self):
        self._score = 0
        self._bonus = 0
        self.__opponent_score_ = 0 
        self.__secret_bonus_word = 'idkfa'

    def __validate_choice_(self, choice):
        activate_bonus = False
        if choice == self.__secret_bonus_word:
            choice= Settings.Choices.confess
            activate_bonus = True
        elif choice not in (Settings.Choices.values_list()):

            # The mentors have little patience for stall tactics. If player doesn't respond 
            # appropriately, assume they choose not to confess.
            print ("The mentor looks at you even more stern and shakes their head."\
                " The voice states flatly, 'Not choosing is still making a choice.'")
            choice = Settings.Choices.stay_silent
        else:
            choice = Settings.Choices(choice)
        return choice, activate_bonus