import random
random.seed()

def Print_Introduction():
    readme = ''
    with open('README.md', 'r') as f:
        for line in f:
            if line[0:5] == '-----':
                break;
            readme += line
    print (readme)

def Calc_Result(player_choice, computer_choice):
    print('game under construction, please come back later')
    return (0,0)

def Get_Computer_Choice():
    #TODO: make the AI smarter - or at least harder to beat
    random_choice = random.range(0,1)
    if random_choice:
        return 'Y'
    else:
        return 'N'

def Play():
    rounds_left = random.randrange(5, 15)
    computer_score = 0
    player_score = 0
    while (rounds_left > 0):
        prompt = 'You are seated in a dark room with a bright light shining in your eyes. A mentor looms over you. Do you confess? (Y/N) '
        player_choice = input(prompt).capitalize()
        
        # Easter Egg for GOD mode.
        if player_choice == 'IDKFA':
            player_score += 1000

        computer_choice = Get_Computer_Choice()

        Calc_Result(player_choice, computer_choice)
        rounds_left -= 1

Print_Introduction()
play_again = 'A'
while True:
    if play_again == 'Q':
        break;
    elif play_again == 'R':
        Print_Introduction()
    else:
        Play()
    print ()
    play_again = input('Choose (Q)uit, (R)ules, or any key to play again? ').capitalize()
