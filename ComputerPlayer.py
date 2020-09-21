import random
import Settings

class Computer_Player(object):
    '''Represents a computer player.'''
    
    @property
    def Bonus(self):
        return(self._bonus)

    @property
    def Score(self):
        return(self._score)

    @property
    def Most_Recent_Choice(self):
        return(self._most_recent_choice)
    
    @Most_Recent_Choice.setter
    def Most_Recent_Choice(self, value):
        self._most_recent_choice = value

    def Set_Bonus(self, value):
        self._bonus = value

    def Choose(self):
        self._most_recent_choice = self.__choose_method_()
        return False 

    def Update_Results(self, round_score, opponent_round_score, opponent_choice):
        self.__opponent_previous_choice_ = opponent_choice
        self.__opponent_score_ += opponent_round_score
        self._score += round_score

    def End_Game(self):
        #TODO: record statistics
        return
        
    def __init__(self):
        random.seed()
        self._bonus = 0
        self._score = 0
        #TODO: set choose method randomly
        #self.__choose_method_ = self.__always_stay_silent_
        #self.__choose_method_ = self.__always_confess_
        self.__choose_method_ = self.__tit_for_that_
        #self.__choose_method_ = self.__random_
        ##self.__choose_method_ = self.__alternate_
        ##self.__choose_method_ = self. __risk_analysis_competition_
        ##self.__choose_method_ = self. __risk_analysis_highest_personal_score_

        self.__opponent_previous_choice_ = None
        self._most_recent_choice = Settings.Choices.confess
        self.__opponent_score_ = 0
    
    ############################ strategy methods 
    
    # This strategy's strong suit is that the opponent is unlikely to be able
    # to predict the computer's choice. However, it will not consistently perform 
    def __random_(self):
        return random.choice(Settings.Choices.list())
    
    # This strategy will generally tie with the opponent simply because it attempts
    # to provide feedback to the opponent in the hopes that the opponent will realize
    # that both confessing is the better choice.
    def __tit_for_that_(self):
        if self.__opponent_previous_choice_ is None:
            self.__opponent_previous_choice_ = Settings.Choices.stay_silent
        return self.__opponent_previous_choice_

    # This strategy can achieve both the hightest and lowest scores, depending 
    # on the other player's choices.
    # See the comments for the __risk_analysis_highest_personal_score_ strategy
    # below for information on why.
    def __always_confess_(self):
        return Settings.Choices.confess

    def __always_stay_silent_(self):
        return Settings.Choices.stay_silent

    def __alternate_(self):
        return self._most_recent_choice.next()

    # The idea here is to evaluate the risk v/s reward, making the choice
    # that can yield the greatest reward, within the acceptable risk, when the 
    # game is viewed as achieveing the highest possible score, with no regard of 
    # the opponent's score.
    # As it turns out, this strategy is STILL no different than stay_silent if the
    # scoring matrix follows the standard Prisoner's Dilemma paradigm where
    # both players get the same reward for making the same choice, and players 
    # are rewarded/peanalized the same amounts for making opposing choices. 
    # The actual values of the rewards/penalties are irrelevant as long as they
    # are consistant because the paradigm dictates:
    # ex: both confess = A points each 
    #     both stay silent = B points each
    #     one confess/other silent = C points for confess, D points for silence
    #   WHERE D > A > B > C
    # So, staying silent will always have less chance of risk (B), with greater 
    # chance of reward (D).
    # Note that this is NOT the BEST possible result (hightest possible score).
    # If both players consistently confess, a higher overall score will be achieved,
    # but this depends on the other player's consitant cooperation.
    def __risk_analysis_highest_personal_score_(self):
        risk_reward = dict()
        final_choice = None
        final_avg_pts = 0
        for c_choice in Settings.Choices:
            points = 0
            # We could maybe be smarter here, but for now just average the
            # points we might receive for this choice 
            for p_choice in Settings.Choices:
                scores = Settings.Get_Score(p_choice, c_choice)
                points += scores[1]
            
            avg_pts = points/len(Settings.Choices)
            if final_choice == None or avg_pts > final_avg_pts:
                final_choice = c_choice
                final_avg_pts = avg_pts
 
        return final_choice

    # The idea here is to evaluate the risk v/s reward, making the choice
    # that can yield the greatest reward, within the acceptable risk, when 
    # the game is viewed as a competition between players for the best score.
    # As it turns out, this strategy is no different than stay_silent if the
    # scoring matrix follows the standard Prisoner's Dilemma paradigm where
    # both players get the same reward for making the same choice, and players 
    # are rewarded/peanalized the same amounts for making opposing choices. 
    # The actual values of the rewards/penalties are irrelevant as long as they
    # are consistant (because we're comparing against the other player).
    # ex: both confess = 2 points each 
    #     both stay silent = -2 points each
    #     one confess/other silent = -3 points for confess, +3 points for silence
    # When we view this as a competition with the other player, getting the same 
    # points (positive or negative) means no overall change in the relative scores 
    # and therefore no real risk. When viewed this way, staying silent means either
    # no net change, or a net gain of 6 points over the other player;  confessing 
    # means no net change or a net loss of 6 points over the other player. 
    # The winning choice is obvious.
    def __risk_analysis_competition_(self):
        risk_reward = dict()
        for c_choice in Settings.Choices:
            risk = 0
            reward = 0
            for p_choice in Settings.Choices:
                scores = Settings.Get_Score(p_choice, c_choice)
                spread = scores[1] - scores[0]
                # find largest reward for this c_choice (by def rewards are > 0)
                if spread > 0 and spread > reward:
                    reward = spread
                # find the lowest risk (by def risks are < 0 - so lowest risk = largest value)
                if spread < 0 and abs(spread) > risk:
                    risk = abs(spread)

            risk_reward[c_choice] = (risk, reward)

        max_acceptable_risk = self.Score - self.__opponent_score_
        best_reward = 0
        lowest_risk = 0
        final_choice = None
        lowest_risk_choice = None
        for choice in risk_reward:
            risk = risk_reward[choice][0]
            reward = risk_reward[choice][1]
            if risk <= lowest_risk:
                lowest_risk = risk
                lowest_risk_choice = choice
            if risk < max_acceptable_risk and reward >= best_reward:
                best_reward = reward
                final_choice = choice

        if final_choice == None:
            final_choice = lowest_risk_choice

        return final_choice
