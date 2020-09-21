# Student's Dilemma

You and a fellow student (played by the computer) have been caught cheating on your final project, however it isn't clear whether one of you plagiarized the other's project or if you conspired together. In an effort to uncover the whole truth, you are both being interrogated. During interrogation you both have are offered a simple choice: confess or stay silent. 

However, there are conditions:
- If you both confess (2 points): Since you both came clean, you will be permitted to submit a new project by the class deadline otherwise you will fail, but you will be allowed to take the course again. 
- If one confesses (-3 points) and one stays silent (3 points). It is assumed that the student who confesses must have plagiarized the other student's work without consent:    
    - The student who confesses will be expelled from the program, banned for life, and worst of all, **will receive a red X on their permanent record**.
    - The student who stays silent is deemed an unknowing victim and will have their final project graded as normal.
- If you both stay silent (-1 points): You will both fail the class and but will be allowed to take the course again, after a 1 year suspension, you will not be expelled from the program, and, thankfully, will avoid the dreaded red X on your permanent record.

But there's more! You are also stuck in a time loop, giving you a Groundhog Day experience where you repeat this exercise a number of times. But beware, somehow due to the Great Mystic forces of the Computer gods, you are not quite starting over each day... your actions add up over the course of five to fifteen chances! 

### Can you outwit the computer and achieve the higher score? Can you find a way to work with the computer to maximize both your scores? Can you discover the rumored secret to success in playing video games?
-----
This game uses an infinite loop as the main loop, marked with the comment '####### MAIN Loop ########' in the source file StudentsDilemma.

This game implements classes. See the files ComputerPlayer.py and HumanPlayer.py which implement the classes ComputerPlayer and Human player respectively.

This game uses a complex regex to load point values from the README.md file in Settings.__parse_rules()


TODO: provide description of code structure and implementation of features here. 
TODO: provide some way to select computer strategies 

TODO: (stretch) record the moves and final scores in a data file 
    - convert each round's score/moves data into an object (round # computer choice, player choice, computer strategy, player name) 
    - convert game info into a list of score objects
    - extend objects to save as JSON
TODO: (stretch) provide some statistical analysis on the recorded games
    - load objects from JSON and parse with pandas or NumPy


TODO: (stretch2) extend data analysis to include computer's strategy
TODO: (stretch2) allow the computer to play itself (to be able to test strategies)
