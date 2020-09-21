import random
import Settings
import ComputerPlayer as cp
import HumanPlayer as hp

def Calc_Score(trigger_p_bonus, trigger_c_bonus):
    if (trigger_p_bonus):
        # the only way the computer bonus gets set is in this code
        if Player.Bonus> 0 or Computer.Bonus > 0:
            Computer.Most_Recent_Choice = Settings.Choices.stay_silent
            Player.Set_Bonus(0)
            Computer.Set_Bonus(Computer.Bonus + 1)
        else:
            Computer.Most_Recent_Choice = Settings.Choices.confess
            Player.Set_Bonus(1)

    scores = Settings.Get_Score(Player.Most_Recent_Choice, Computer.Most_Recent_Choice)
    bonuses = (Player.Bonus, Computer.Bonus)
    print(f"scores {scores}  bonuses {bonuses}")
    round_totals = [a + b for a, b in zip(scores, bonuses)]
    return round_totals[0], round_totals[1]

def Play():
    # Random number of rounds to help keep players guessing
    rounds_left = random.randint(5, 15)
    running_score = [0,0] 

    while (rounds_left > 0):
        trigger_p_bonus, trigger_c_bonus = Player.Choose(), Computer.Choose()
        p_round_score, c_round_score = Calc_Score(trigger_p_bonus, trigger_c_bonus)
        End_Round(p_round_score, c_round_score)
        rounds_left -= 1
    End_Game()

def End_Round(p_round_score, c_round_score):
    Computer.Update_Results(c_round_score, p_round_score, Player.Most_Recent_Choice)
    Player.Update_Results(p_round_score,c_round_score, Computer.Most_Recent_Choice)

def End_Game():
    Player.End_Game() 
    Computer.End_Game()

####### Initialize #######
random.seed()
play_again = 'r'
Settings.Load()

####### MAIN Loop ########
while True:
    Computer = cp.Computer_Player()
    Player = hp.Human_Player()

    if play_again == 'r':
        Player.Report(Settings.Rules)
    elif play_again == 'p':
        Play()
    else:
        break;

    print() 
    play_again = Player.Prompt('Choose play (p), show rules (r), or press any key to quit> ').lower()

