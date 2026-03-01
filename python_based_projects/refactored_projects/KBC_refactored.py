questions=[ ['1. What is the capital of Australia?','A. Bathurst ','B. Balmain','C. Canebrra ','D. Geelong','C'],
           ['2. Which planet is known as the "Evening Star"?','A. Venus', ' B. Mercury','C. Earth',' D. Mars','B'],
           ['3. What is the largest ocean on Earth?','A. Pacific Ocean',' B. Indian Ocean','C. Atlantic','      D. Arctic','A'],
           ['4. Who is known as the "Father of the Indian Constitution"?','A. Dr. B.R. Ambedkar' ,' B. Mahatma Gandhi ','C. Jawaharlal Nehru' ,'  D. Madan Mohan Malviya','A'],
           ['5. In which city was the first modern Olympic Games held?','A. Brazil','  B. Athens','C. America ','D. Australia','B'],
           ['6. Who was the first Indian to win an Oscar?','A. Bhanu Athaiya','B. Satyajit Ray','C. AR Rahman','    D. Gulzar','A'],
           ['7. Which planet is known as the Red Planet?','A. Venus','B. Earth','C. Mars',' D. Jupiter','C'],
           ['8. Who wrote the play \'Romeo and Juliet\'?','A. William Shakespeare','B. Charles Dickens','C. Jane Austen','        D. Mark Twain','A'],
           ['9. Which country hosted the 2016 Summer Olympics?','A. China',' B. Brazil','C. Russia','D. Engalnd','B'],
           ['10. Which Indian state is known as the "Land of Five Rivers"?','A. Punjab',' B. Rajasthan','C. Gujarat','D. Uttar Pradesh','A']]
prize=[1000,2000,3000,5000,10000,20000,40000,80000,160000,320000]
dhanrashi=0
options=['A','B','C','D']
can_use=True
can_ask=True
while True:
 inp=input('Kya aap is khel ka aarambh karna chahte hai? \nHAA ya NAA me uttar dijiye.\n').upper()
 if inp=='HAA':
  i=0
  while i in range(len(questions)):
   ques=questions[i]
   print(f'{ques[0]} 💰=₹{prize[i]}  TOTAL💵=₹{dhanrashi}\n{ques[1]}      {ques[2]}\n{ques[3]}      {ques[4]}')
   if can_ask==True:
    ans=input("Prashan ka uttar dijiye A/a,B/b,C/c ya D/d me dijiye anytha quit karne ke liye Q/q aur LifeLine(50-50) ke liye 5050 dbaye!!\n").upper()
   if can_ask==False:
    ans=input("Prashan ka uttar dijiye A/a,B/b,C/c ya D/d me dijiye anytha quit karne ke liye Q/q ab apke pass koi life line nhi hai!!\n").upper()

   if ans==ques[5]:
    print(f"Mahashya apne ₹{prize[i]} rupay ki 💰 dhan rashi prapt kar li hai ")
    dhanrashi=dhanrashi+prize[i]
    i=i+1
   elif ans=='Q':
    print(f'Aap apne saath ₹{dhanrashi} dhanrashi ghar lekar jaa rhae hai') 
    exit()   
   if can_use==True and ans=="5050":
    can_ask=False
    can_use=False 
    while True:
     import random
     choice1=random.choice(options)
     choice2=random.choice(options)
     if choice1==choice2:
      continue
     elif choice1==ques[5] or choice2==ques[5]:
      continue
     else:
      print(f'({choice1}) aur ({choice2}) galat vikalp hai')
      break
   elif ans!='A'and ans!='B' and ans!='C' and ans!='D':
    print('Kya apko type karna nhi aata 🤬')    
   elif ans!=ques[5]:
    print(f'Mahashaya yeh uttar galat hai shi uttar hai \'{ques[5]}\'')
    if i<5:
     print('Apko khali haat ghar jana hoga 😔')
    if i>=5 and i<10:
     print(f'App apne saath ₹11000 ki 💰 dharashi lekar jaa rhe hai')
    if i==10:
     print(f'App apne saath ₹11000 ki 💰 dharashi lekar jaa rhe hai') 
    exit() 
   if i==5 :
    print('Mubarak aap khel ka pahla  padav paar kar chuke hai')
   elif i==10:
    print('Mubarak aapne is khel ka dusra padav paar karke ise samapt kar diya hai') 
 elif inp=='NAA':
  break
 else:
  print('Kya apko type karna nhi aata!!🤬') 
   
   
 
