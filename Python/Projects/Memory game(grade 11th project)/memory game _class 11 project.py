import random #importing random module for shuffling the cards
import time

#asking for the player's name
d={}
score={}
key =input('player no.')
value = input('enter the name of player')
d[key]=value
score[value]=0
print(d)
    
#1 defining the sizze of the board
size=int(input('enter the board dimension (eg: for 4X4 enter 4 ; even dimension only)'))
if size%2!=0:
    print('invalid input..try again')
    size=int(input('enter the board dimension (eg: for 4X4 enter 4 ; even dimension only)'))

#2 creating symbols for the board(making a list of capital letters as the symbols)
symbols=[]
for i in range((size*size)//2):
    symbols.append(chr(65+i))                #---> chr(65)='A' , this creates a list [A,B,C,D,E,F,G,H]

#3 duplicate the symbols
symbols=symbols*2                            #---> [A,B,C,D,E,F,G,H,A,B,C,D,E,F,G,H]

#4 shuffling the symbols randomly
random.shuffle(symbols)

#5 creating a game board as a 2d list
b=()
board=list(b)
for i in range(0,len(symbols),size):
   row=symbols[i:i+size]
   board.append(row)

#6 creating revealing board(helps to keep track of the revealed values)
revealed=[]
for i in range(size):
    row=[]
    for j in range(size):
        row.append(False)
    revealed.append(row)

#7 keeping a count of req. data
attempts=0
pairs_matched=0
total_pairs=(size*size)//2

# Starting the timer
start_time = time.time()

print()
print('~~ MEMORY GAME STARTED !! ~~')
print()


#8 MAIN GAME LOOP:
while pairs_matched<total_pairs:

  ##8.1 displaying the board with revealed and unrevealed vales
  for i in range(size):
      row=[]
      for j in range(size):
        if revealed[i][j]==True:
              row.append(board[i][j]+' ')
        else:
              row.append('* ')
      print(' '.join(row))
  print()

  ##8.2 players selects the first card
  while True:
       value=input('select FIRST card (column,row):')
       coords=value.split(',')
       col1=int(coords[0])-1
       row1=int(coords[1])-1
       if 0<=row1<size and 0<=col1<size and not revealed[row1][col1]:
           break
       else:
           print('invalid input ..TRY AGAIN')

  revealed[row1][col1]=True

  ##8.3 displaying the board after first entry
  for i in range(size):
      row=[]
      for j in range(size):
        if revealed[i][j]==True:
              row.append(board[i][j]+' ')
        else:
              row.append('* ')
      print(' '.join(row))

  ##8.4 players selects the second card
  while True:
       value=input('select SECOND card (column,row):')
       coords=value.split(',')
       col2=int(coords[0])-1
       row2=int(coords[1])-1
       if 0<=row2<size and 0<=col2<size and not revealed[row2][col2]:
           break
       else:
           print('invalid input ..TRY AGAIN')

  revealed[row2][col2]=True

  ##8.5 displaying the board after second entry
  for i in range(size):
      row=[]
      for j in range(size):
        if revealed[i][j]==True:
              row.append(board[i][j]+' ')
        else:
              row.append('* ')
      print(' '.join(row))

  ##8.6 checking if the pairs match
  if board[row1][col1]==board[row2][col2]:
      print('its a match')
      pairs_matched+=1
      score[d[key]] += 1 
      
  else:
      print('no match...try again')
      revealed[row1][col1]=False
      revealed[row2][col2]=False
      

  attempts += 1
  
# Ending the timer
end_time = time.time()

# Calculate total elapsed time
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

#9 end of the game
print()
print('Congratulations! You found all pairs in ',attempts,'attempts')
print('Time taken:',minutes, 'minutes and ',seconds,'seconds.')
print('Final Score:', score)
        
    

    

    

        


    
        
         
         
         
         
    


