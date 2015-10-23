
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


rule = pd.read_csv("rules.csv") #data install
index0 =rule["Unnamed: 0"]
del rule["Unnamed: 0"]
index0.name = "playercard"
columns0 = rule.columns
columns0.name="dealercard"
rule = pd.DataFrame(rule.values,index=index0,columns=columns0)
    #deck = np.zeros((24,13))



# In[2]:

rule.ix["Pair8"]["10"]="P" #これはスプリットのがよさそう
rule.ix["Pair8"]["1"]="P"  ##これはスプリットのがよさそう
rule.ix["Hard11"]["10"]="Dh" #or "Dh" どっちでもいいっぽい
rule.ix["PairA"]["1"] = "P" #must sPrit !!!

#rule


# In[3]:

##making deck
def makedeck():
    deck0 = np.arange(1,11,1,dtype=int)
    deck0 = np.append(deck0,10)
    deck0 = np.append(deck0,10)
    deck0 = np.append(deck0,10)
    ##24sets of 1:13 which means 6 decks
    deck = np.r_[deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0,deck0, deck0]
    np.random.shuffle(deck)
    return deck
deck=makedeck()

##draw the card
def draw(deck1):
    global deck # deck is global
    drawcard_number = np.random.randint(len(deck1)) #  0〜len(deck)-1 の整数を1個生成
    drawcard = deck[drawcard_number]
    deck = np.delete(deck1, drawcard_number)
    return drawcard



# In[4]:

##making the score of cards ( not considering whether small or big )
##soft18 =18

def make_score(cards):
    score_0 = sum(np.select([cards > 1],[cards]))
    number_of_1 = sum(np.select([cards == 1],[cards]))
    if score_0>10:
        score = score_0 + sum(np.select([cards == 1],[cards]))
    if score_0<11 and number_of_1 == 1:    #soft18 =18
        score = score_0 + 11
    elif score_0<11 and number_of_1 > 1:
        score = score_0
        score = number_of_1 - 1 + score_0
        if score >10:
            score = score + 1
        else: score = score +11
    elif number_of_1 ==0:
        score =score_0 
    return score


# In[5]:

##Judge "pair or soft or hahrd"
## when 2 cards

def pair_soft_hard_0(playercard):
    if playercard[0]==playercard[1] and playercard[0]==1 and len(playercard)==2:
        return "PairA"
    elif playercard[0]==playercard[1] and len(playercard)==2:
        string = "Pair" + str(playercard[0])
        return string        
    elif sum(np.select([playercard == 1],[playercard]))>0:
    #elif np.selectplayercard[0]==1 or playercard[1]==1:
        string="Soft"
        count = playercard[0]+playercard[1]+10
        string = string + str(count)
        return string
    else :
        string="Hard"
        count = playercard[0]+playercard[1]
        string = string+str(count)
        return string

        
## Judge "soft or hard or burst"
## cards more than 3

def soft_hard_burst(playercard):
    ## cards have 1
    if sum(np.select([playercard == 1],[playercard]))>0:
        criterion = sum(np.select([playercard == 1],[playercard])) - 1 + sum(np.select([playercard != 1],[playercard]))
        if criterion < 11:
            string="Soft"
            count =make_score(playercard)
            #count = playercard[0]+playercard[1]+10
            string = string + str(count)
            if count < 22:
                return string
            else:
                return "burst"
        elif criterion >10:
            string = "Hard"
            count =make_score(playercard)
            string = string + str(count)
            if count < 22:
                return string
            else:
                return "burst"
    ## cards have no 1
    elif sum(np.select([playercard == 1],[playercard]))==0:
        string="Hard"
        count = sum(playercard)
        string = string+str(count)
        if count < 22:
            return string
        else:
            return "burst"


# In[6]:

"""
changing the player cards depending on options, such as...
H   Hit 
S   Stand 
P   Split 
Dh  Double if possible, otherwise Hit
Ds  Double if possible, otherwise Stand
"""
def p_drawer(string,pclist_1): #string={H,S,P,Dh,Ds} playercard =np.array[3,4]
    global deck
    #pclist_1 = [[betmoney, np.array(1,3)],[betmoney, np.array(1,3)]]
    if string =="H":
        pclist_1[1] = np.append(pclist_1[1],draw(deck))
    elif string =="S":
        return pclist_1
    elif string =="Dh":
        if len(pclist_1[1])==2:
            pclist_1[1] = np.append(pclist_1[1],draw(deck))
            pclist_1[0] = pclist_1[0] + pclist_1[0]
        elif len(pclist_1[1])>2:
            pclist_1[1] = np.append(pclist_1[1],draw(deck))
    elif string =="Ds":
        if len(pclist_1[1])==2:
            pclist_1[1] = np.append(pclist_1[1],draw(deck))
            pclist_1[0] = pclist_1[0] + pclist_1[0]
        elif len(pclist_1[1])>2:
            return pclist_1
    return pclist_1


# In[7]:

# player action
def p_action(pclist,dealercard):
    global deck
    newlist=[]
    i =0
    #print "pclist in p_action", pclist 
    while True:
        # the first stage of 2 cards and not pairA
        if len(pclist[i][1])==2 and (pclist[i][1][0]!=1 and pclist[i][1][1]!=1): 
            raw_string = pair_soft_hard_0(pclist[i][1])
            col_string = str(dealercard[0])
            string = rule.ix[raw_string][col_string]
            if string == "P":
                arraynp0 = np.array([pclist[i][1][0],draw(deck)],dtype=int)
                arraynp1 = np.array([pclist[i][1][1],draw(deck)],dtype=int)
                pclist.append([pclist[i][0],arraynp0])
                pclist.append([pclist[i][0],arraynp1])
                del pclist[i]
            else:
                pclist[i] = p_drawer(string,pclist[i])
        
        # the first stage of 2cards of pairA ( beacuse, spriting of pairA can hit only one card for each )
        elif len(pclist[i][1])==2 and pclist[i][1][0]==1 and pclist[i][1][1]==1:
            raw_string = pair_soft_hard_0(pclist[i][1])
            col_string = str(dealercard[0])
            string = rule.ix[raw_string][col_string] 
            #if you got pairA , you must sprit them. However, in this case, you can choose "P" or "H" or whatever.
            if string == "P": 
                newcardlist=[]
                newcardlist.append(1)
                newcardlist.append(1)
                newcardlist = np.array(newcardlist)
                np.select([newcardlist == 1],[newcardlist])

                equals1counter = 0
                #drawing until number of A equals number of not A
                while equals1counter < sum(np.select([newcardlist == 1],[newcardlist])):    
                    card = draw(deck)
                    newcardlist = np.append(newcardlist,card)
                    if card !=1:
                        equals1counter = equals1counter + 1
                
                newlist=[]
                newcardlist.sort() #newcardlist=[1,1,1,6,8,10] 
                for i in range(sum(np.select([newcardlist == 1],[newcardlist]))):
                    arraynp0 = np.array([1,newcardlist[-(i+1)]],dtype=int)
                    newlist.append([pclist[0][0],arraynp0])
                    
                return newlist
            else:
                pclist[i] = p_drawer(string,pclist[i])

        elif len(pclist[i][1])>2: # or state after split
            raw_string = soft_hard_burst(pclist[i][1])
            if raw_string != "burst": 
                col_string = str(dealercard[0])
                string = rule.ix[raw_string][col_string]
                pclist[i] = p_drawer(string,pclist[i])
        
        # while done condition
        i = i+1
        if i == len(pclist): 
            newlist = pclist
            return newlist


# In[8]:

"""
I am sorry about this rusty function
"""
def pplay(pclist3,dealercard):
    after=[]
    before=[]
    after=pclist3[:]
    for i in range(7):
        #Pair A can hit only one card
        if len(after)==2:
            if after[0][1][0]==1 and after[1][1][0]==1 and len(after[0][1])==2 and len(after[1][1])==2:
                return after
        after = p_action(after,dealercard)
    return after
            


# In[9]:

# for dealer judge soft or hard
def soft_or_hard(card):
    if sum(np.select([card == 1],[card]))>0:
        hyoukajiku = sum(np.select([card == 1],[card])) - 1 + sum(np.select([card != 1],[card]))
        if hyoukajiku < 11:
            string="Soft"
        else:
            string = "Hard"
        return str(string)
    elif sum(np.select([card == 1],[card]))==0:
        return "Hard"


# In[10]:

def dplay(dealercard):
    d_after = dealercard
    while True:
        d_before = d_after
        dscore = make_score(d_before)
        if dscore >17: #not burst 
            d_after=d_before
            break
        elif (dscore == 17) and (soft_or_hard(d_before)=="Soft"):
            #d_after = np.append(d_before,draw(deck)) #d can hit
            d_after=d_before #d can not hit
            break
        elif dscore == 17 :
            break
        elif dscore <17: # d must hit
            d_after = np.append(d_before,draw(deck))
        del d_before
    return d_after


# In[11]:

#battle !
def judgemoney(pclist,dealercard):
    money=0
    dscore = make_score(dealercard)
    for i in range(len(pclist)):
        pscore = make_score(pclist[i][1])
        #Player burst
        if pscore>21: money = money - pclist[i][0]
        elif len(pclist[i][1])==2 and pscore==21: #P = BJ
            if len(dealercard)==2 and dscore==21: #D = BJ
                money = money
            else:
                money = money + 1.5 * pclist[i][0]
        #P = 21 or less
        elif pscore<22:         
            if len(dealercard)==2 and dscore==21: #D = BJ
                money = money - pclist[i][0]
            elif dscore > 21:
                money = money + pclist[i][0]  #D Burst
            elif pscore > dscore:
                money = money + pclist[i][0] #P wins Burst
            elif pscore < dscore:            #D wins
                money = money - pclist[i][0]    
    return money
            


# In[12]:

def count(pclist,dealercard):
    plus=0
    minus=0
    #count for playercard
    for p in pclist:
        where_minus =np.where((p[1]>1)&(p[1]<7)) 
        minus= -len(p[1][where_minus])
        where10  = np.where((p[1]==10))
        plus = len(p[1][where10])
        where1 =np.where(p[1]==1)
        plus = plus + len(p[1][where1])
    
    #count for dealercard
    where_minus = np.where((dealercard>1)&(dealercard<7))
    minus = minus - len(dealercard[where_minus])
    where10 = np.where((dealercard==10))
    plus = plus + len(dealercard[where10])
    where1 = np.where((dealercard==1))
    plus = plus + len(dealercard[where1])

    
    return plus + minus


# In[22]:

def play(times):
    global deck
    deck = makedeck()
    mhistory =[]
    bet = 10
    totalmoney = 400
    counter = 0
    for i in range(times):
        playercard = np.array([draw(deck)],dtype=int)
        playercard = np.append(playercard,draw(deck))
        #playercard = np.array([5],dtype=int)
        #playercard = np.append(playercard,5) # for making Pair3
        #dealercard = np.array([10],dtype=int)
        #dealercard = dplay(dealercard) #for making Dealer card A        
        pclist=[[bet,playercard]]
        dealercard = np.array([draw(deck)],dtype=int)
        dealercard = dplay(dealercard)
        pclist = pplay(pclist,dealercard)
        #print "pclist in play", pclist,"   dclist in play", dealercard
        
        gainmoney = judgemoney(pclist,dealercard)
        
        ########################
        #######counting! change your bet#########
        #print "cards ",pclist,dealercard
        #print "this_Game count",count(pclist,dealercard)
        #print "counter so far ",counter
        counter = counter + count(pclist,dealercard)
        #print "total_counter",counter        
        if counter< -15:
            bet= 20
        else:
            bet =10
        
        ###################################
        #####battle only when fewer decks#####
        if(len(deck)<52*4) and counter< -10:
            totalmoney = totalmoney + gainmoney
        ################################### 
        
        
        if totalmoney ==0:
            print "total money bacame 0!!! OMG!!!!!!"
            break
        
        mhistory.append(totalmoney)
        #print dealercard, pclist
        if(len(deck)<52*1.5):
            deck = makedeck()
            counter =0
            return mhistory
        #print "len deck  ",len(deck)
    return mhistory


# In[23]:

"""
basically, Player has an advantage when there are a lot of 10s in deck
on the other hand, the dealer tends to win when there are a lot of smaller cards in the deck.
This is because the dealer hardly get into burst because of smaller cards
Furthermore, player's double is not so effective in such a condition.
To sum up, in this code, if count gets more plus, player loses more.
"""

start = time.time()
nparray=np.array([])
for i in range(3000): # simulation times
    mh = play(10000)
    lastm = mh[-1]
    npmh = np.array([lastm])
    nparray=np.r_[nparray,npmh]

plt.hist(nparray,bins = 80)
plt.title("Histgram")
plt.xlabel("acqired_money")
plt.ylabel("frequency")
print "average  ", np.mean(nparray) # np.average(nparray)
#print "play_times  ",len(nparray)
#print mhistory
elapsed_time = time.time() - start


print "elapsed time  ",elapsed_time

plt.show()


# In[17]:




# In[15]:


plt.hist(counter22,bins = 50)
plt.show()


# In[75]:

ko = np.array(counter22,dtype=int)


# In[76]:

sum(np.select([ko > 10],[ko]))


# In[78]:

sum(np.select([ko > -10],[ko]))


# In[62]:

ko


# In[ ]:



