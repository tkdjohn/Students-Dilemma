import random
random.seed()

def Introduction():
    readme = ''
    with open('README.md', 'r') as f:
        for line in f:
            if line[0:5] == '-----':
                break;
            readme += line
    print (readme)

def Play():
    iterations = random.randrange(5, 15)
    while (iterations > 0):
        print ('iteration ', iterations)
        iterations-= 1

play_again = "Y"
while play_again[0:1] == "Y":
    Play()
    play_again = input("Would you like to play again? (Y/N) ").capitalize()
    
