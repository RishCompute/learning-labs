import math_eval as me
def main_run():

  while True: 
   try: 
    ask=input('Enter equation or for history press "h" for exit press "ex" : ')
    ANS=me.safe_compute(ask)
    if ask=='h':
     file=open('calhistory','r') 
     if  file.readlines()==[]:
        print('No History')
     else:
       file=open('calhistory','r')    
       for index,history in enumerate(file.readlines()):
        print(f'{index+1}:{history.strip()}')
       file.close() 
       clearing_ask() 
          

    elif ask=='ex':
     exit() 

    else :
     print(f'{ask}={ANS}')
     with open('calhistory','a') as f:
      f.write(f'{ask}={ANS}\n')
   except ZeroDivisionError:
     print("Cannot be divide by zero")
         



def clearing_ask():
    while True: 
     asking=input('\nfor clearing history press "c"/press "e" to exit the main menu: ')
     if asking=='c':
      user_input=input('for clearing all press "a" / to clear a particular history press "p": ')
      clearhistory_logic(user_input)
     elif asking=='e':
       break
     
def clearhistory_logic(user_input):
   
    if user_input=='a':
       with open('calhistory','w') as file:
        file.truncate(0)
      
    elif user_input=='p':
       with open('calhistory','r') as file:
        for index,i in enumerate(file.readlines()):
         print(f'{index+1}:{i.strip()}')
        lastask=(input('Enter the no of the history you want to delete: \n'))
        with open('calhistory', 'r') as f:
         lines = f.readlines()
         if not (lastask.isdigit() and 1 <= int(lastask) <= len(lines)):
                print("Wrong Input")
                return
        with open('calhistory', 'w') as f:
         for i, line in enumerate(lines,1):
           if i != int(lastask):  
            f.write(line) 
           
             

main_run()    





    


