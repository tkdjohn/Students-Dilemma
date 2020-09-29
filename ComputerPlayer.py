import random
import Settings

class ComputerPlayer(object):
    '''Represents a computer player.'''

    @property
    def Bonus(self):
        return(self.bonus)

    @property
    def Score(self):
        return(self.score)

    @property
    def MostRecentChoice(self):
        return(self.mostRecentChoice)

    @MostRecentChoice.setter
    def MostRecentChoice(self, value):
        self.mostRecentChoice = value

    def SetBonus(self, value):
        self.bonus = value

    def Choose(self):
        self.mostRecentChoice = self.chooseMethod()
        return False

    def UpdateResults(self, roundScore, opponentRoundScore, opponentChoice):
        self.opponentPreviousChoice = opponentChoice
        self.opponentScore += opponentRoundScore
        self.score += roundScore

    def EndGame(self):
        #TODO: record statistics
        return

    def __init__(self):
        random.seed()
        self.bonus = 0
        self.score = 0

        strategies = [
            self.alwaysstay_silent,
            self.alwaysConfess,
            self.alwaysConfess,
            self.alwaysConfess,
            self.alternate,
            self.riskAnalysisCompetition,
            self.riskAnalysisHighestPersonalScore]

        self.chooseMethod = random.choice(strategies)
        ##DEBUG print(self.chooseMethod)
        self.opponentPreviousChoice = None
        self.mostRecentChoice = Settings.Choices.confess
        self.opponentScore = 0

    ############################ strategy methods

    # This strategy's strong suit is that the opponent is unlikely to be able
    # to predict the computer's choice. However, it will not consistently perform
    def random(self):
        return random.choice(Settings.Choices.list())

    # This strategy will generally tie with the opponent simply because it attempts
    # to provide feedback to the opponent in the hopes that the opponent will realize
    # that both confessing is the better choice.
    def titForThat(self):
        if self.opponentPreviousChoice is None:
            self.opponentPreviousChoice = Settings.Choices.stay_silent
        return self.opponentPreviousChoice

    # This strategy can achieve both the hightest and lowest scores, depending
    # on the other player's choices.
    # See the comments for the riskAnalysisHighestPersonalScore strategy
    # below for information on why.
    def alwaysConfess(self):
        return Settings.Choices.confess

    def alwaysstay_silent(self):
        return Settings.Choices.stay_silent

    def alternate(self):
        return self.mostRecentChoice.next()

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
    def riskAnalysisHighestPersonalScore(self):
        riskReward = dict()
        finalChoice = None
        finalAvgPts = 0
        for cChoice in Settings.Choices:
            points = 0
            # We could maybe be smarter here, but for now just average the
            # points we might receive for this choice
            for pChoice in Settings.Choices:
                scores = Settings.GetScore(pChoice, cChoice)
                points += scores[1]

            avgPts = points/len(Settings.Choices)
            if finalChoice == None or avgPts > finalAvgPts:
                finalChoice = cChoice
                finalAvgPts = avgPts

        return finalChoice

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
    def riskAnalysisCompetition(self):
        riskReward = dict()
        for cChoice in Settings.Choices:
            risk = 0
            reward = 0
            for pChoice in Settings.Choices:
                scores = Settings.GetScore(pChoice, cChoice)
                spread = scores[1] - scores[0]
                # find largest reward for this copmuter choice (by def rewards are > 0)
                if spread > 0 and spread > reward:
                    reward = spread
                # find the lowest risk (by def risks are < 0 - so lowest risk = largest value)
                if spread < 0 and abs(spread) > risk:
                    risk = abs(spread)

            riskReward[cChoice] = (risk, reward)

        maxAcceptableRisk = self.Score - self.opponentScore
        bestReward = 0
        lowestRisk = 0
        finalChoice = None
        lowestRiskChoice = None
        for choice in riskReward:
            risk = riskReward[choice][0]
            reward = riskReward[choice][1]
            if risk <= lowestRisk:
                lowestRisk = risk
                lowestRiskChoice = choice
            if risk < maxAcceptableRisk and reward >= bestReward:
                bestReward = reward
                finalChoice = choice

        if finalChoice == None:
            finalChoice = lowestRiskChoice

        return finalChoice
