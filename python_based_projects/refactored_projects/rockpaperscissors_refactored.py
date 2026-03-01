import random
ROCK='r'
PAPER='p'
SCISSOR='s'
table={ROCK:'🪨',PAPER :'📰',SCISSOR :'✂️'}
table2=tuple(table.keys())

def get_user_choice():
 while True:
  a=input("Rock paper and scissor (r/p/s)?  ").lower()
  if a in table:
    return a
  print("Invalid Choice")

def get_computer_choice():
 return random.choice(table2)
 
def game_logic(a,k):
 print( "You chose:",table[a],"\nComputer chose:",table[k])
 if a==ROCK and k==SCISSOR or a==SCISSOR and k==PAPER or a==PAPER and k==ROCK:
   print("You Won!!")
 elif a==k:
   print("Draw!!")
 else:
   print("You Lose!!")

def continue_play():
 while True:
  ask=input("Wanna play again(y/n)? ").lower()
  if ask=='y':
   break
  elif ask=='n':
   exit()
  else:
   print("Invalid choice")     
 
def play_game():
 while True:
  user_choice=get_user_choice() #to store the return value
  computer_choice=get_computer_choice()# to store the return value of computer
  game_logic(user_choice,computer_choice)
  continue_play()

play_game()

     

 

 
   
   
      
     
     








   
      
     
     


