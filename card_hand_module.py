
import numpy as np 
import random as rand 

class card: 

    suits = ['H','S','D','C']
    ranks = [ str(j) for j in range(2,10) ] + ['T', 'J','Q','K','A']  

    def __init__ (self, inputstr ) : 
        ''' Hearts, Spades, Diamonds, Clubs -- HSDC and then A,2-9,T,J,Q,K'''
        self.suit = inputstr[0] 
        self.rank = inputstr[1] 

    def __str__ (self): 
        return self.suit + self.rank  

    def __eq__(self,other):
        return self.suit == other.suit and self.rank == other.rank
        

    def get_random(): 
        return card( rand.choice(card.suits) + rand.choice(card.ranks)  ) 

    def isSame(card2): 
        if self.suit == card2.suit: 
            if self.rank == card2.rank: 
                return True
        return False


class hand: 
    help_dict = {str(num):num for num in range(2,10) } 
    help_dict['T']=10; 
    help_dict['J']=11; help_dict['Q']=12; help_dict['K']=13; 
    help_dict['A'] = 14 ; 


    def __init__ (self, card_list ) : 
        self.card_list = card_list 
        self.rank_list = [ hand.help_dict[c.rank] for c in self.card_list ] #number val of rank

    def __str__(self): 
        return ','.join([ c.suit + c.rank  for c in self.card_list ] ) 

    def addCard(self,c ): 
        self.card_list.append( c )
        self.rank_list.append( hand.help_dict[ c.rank ] ) 

    def removeCard(self,c): 
        if c in self.card_list: 
            self.card_list.remove( c) 
            self.rank_list.remove( hand.help_dict[c.rank] ) 

    def copy(self): 
        newhand = hand([]) 
        for c in self.card_list: 
            newhand.addCard( c ) 
        return newhand

    def isAce(self) : 
        for c in self.card_list: 
            if c.rank == 'A' : 
                return True
        return False 

    def isDuplicate(self): 
        for j, c in enumerate( self.card_list ): 
            if c in self.card_list[j+1:]:
                return True
        return False

    # functions to determine hand. 

    def isRoyalFlush(self): 
        return self.isStraightFlush() and sum(self.rank_list) == 60 

    def isStraightFlush(self): 
        return self.isStraight() and self.isFlush(); 


    def isKind(self,n):
        '''n=4 would be checking for 4 of a kind exactly.'''
        # rank_list = [ hand.help_dict[c.rank] for c in self.card_list  ]
        rank_list = self.rank_list 
        for r in rank_list: 
            if rank_list.count(r) == n: 
                return True

        return False 

    def isFullHouse(self): 
        return self.isKind(3) and self.isKind(2) 

    def isFlush(self):
        return [c.suit for c in self.card_list  ].count( self.card_list[0].suit ) == 5  

    def isStraight(self): 
        rank_list = self.rank_list 
        rank_list.sort() 
        # print( rank_list ) 
        # ace exception 
        if self.isAce():
            # print( 'There is ace' ) 
            if [ r - 2 for r in rank_list[:-1] ] == [j for j in range(4) ] : 
                return True
        return [ r - rank_list[0] for r in rank_list] == [j for j in range(5) ] 

    def isTwoPair(self): 
        # rank_list = [ hand.help_dict[c.rank] for c in self.card_list  ]
        rank_list = self.rank_list 
        cnt_each = [ rank_list.count(l) for l in rank_list ] 
        return cnt_each.count(2) == 4  # each card in pair appears twice.  


    def handRank(self): 

        if len(self.card_list) == 0 :  # empty hand to begin comparison
            return -1 

        if len(self.card_list) != 5: 
            print( 'Warning not 5 cards in hand') 
            return -1 

        if self.isDuplicate():
            print( 'Warning duplicate present. Nonphysical hand.' ) 
            return -1 

        if self.isRoyalFlush(): 
            return 9 
        elif self.isStraightFlush(): 
            return 8 
        elif self.isKind(4): 
            return 7 
        elif self.isFullHouse(): 
            return 6 
        elif self.isFlush(): 
            return 5
        elif self.isStraight(): 
            return 4 
        elif self.isKind(3): 
            return 3 
        elif self.isTwoPair(): 
            return 2
        elif self.isKind(2): 
            return 1 
        else: 
            return 0 


    def holdEmBestHand(self): 
        # Returns best hand
        # If less than 5, randomly picks cards to complete hand
        # Else, finds 5 card hand from all present
        # returns best hand  

        if len(self.card_list) < 5: 
            temphand = self.copy() 
            while len(temphand.card_list) < 5: 
                rc = card.get_random() 
                if not (rc in temphand.card_list): 
                    temphand.addCard( rc ) 
            return temphand 


        elif len(self.card_list) == 5: 
            return self  

        # must pick best pair and high card !!! 

        # if len > 5  assume less than 8
        elif len(self.card_list) == 6:
            curhand = hand([]) 
            
            for j in range(len(self.card_list) ): 
                temphand = self.copy()
                temphand.removeCard( self.card_list[j] ) 

                if temphand.isBetter(curhand): 
                    curhand = temphand
            
            return curhand 


        else: # for 7 cards 
            curhand = hand([]) 
            
            for j in range(len(self.card_list) ): 
                temphand = self.copy()
                temphand.removeCard( self.card_list[j] ) 
                for k in range(j+1,len(self.card_list) ):
                    temphand2 = temphand.copy() 
                    temphand2.removeCard( self.card_list[k] ) 

                    if temphand2.isBetter(curhand): 
                        curhand = temphand2 
            
            return curhand 

    def isBetter(self, hand2) : 
        ''' does self beat hand2 (no for push)'''

        rank1 = self.handRank() 
        rank2 = hand2.handRank()

        # print( self, rank1, hand2, rank2) 


        if rank1 > rank2: 
            return True
        elif rank1 == rank2: 
            return self.tieBreak(hand2, self.handRank() ) 

        else: 
            return False 

    def tieBreak(self, hand2, hand_rank): 
        ''' help function for is Better 
            returns true if self is better than hand2 ''' 

        list1 = self.rank_list[:] 
        list2 = hand2.rank_list[:] 

        kind_rank = lambda mylist: max( ( (mylist.count(j),j) for j in mylist ) )[1]

        if hand_rank == 0: 
            list1.sort( reverse=True ) 
            list2.sort( reverse=True ) 

            return list1 > list2    # split pots are considered loss!!!! 

        elif hand_rank == 1: 
            # find rank of a Kind paring

            if kind_rank( list1 ) > kind_rank( list2 ) : 
                return True 
            elif kind_rank( list1 ) ==  kind_rank( list2 ) : 
                return self.tieBreak( hand2, 0 ) # find high card 
            else: 
                return False 


        elif hand_rank == 2: # two pair 
            def findpairs( rank_list ) :
                mylist = rank_list[:] 
                help_list = list( set( mylist ) ) 
                for elm in help_list: 
                    mylist.remove( elm ) 
           
                return mylist

            list1 = findpairs( list1 ) 
            list2 = findpairs( list2 ) 
           
            list1.sort( reverse=True) ;
            list2.sort( reverse=True) ; 

            if list1 == list2: 
                return  self.tieBreak(hand2,0) 
               
            else: 
                return list1 > list2  

        elif hand_rank == 3: # three of a kind 
            return self.tieBreak(hand2,1) 

        elif hand_rank == 4: # straight 
            sum1 = sum(list1) 
            sum2 = sum(list2) 
            if self.isAce() : 
                sum1 -= 14 
            if hand2.isAce(): 
                sum2 -= 14 

            if sum1 > sum2: 
                return True
            elif sum1 == sum2: 
                return self.tieBreak(hand2,0) 
            else: 
                return False 

        elif hand_rank == 5: # flush 
            return self.tieBreak(hand2,0) 

        elif hand_rank == 6:  # full house  
            return self.tieBreak(hand2,1) 

        elif hand_rank == 7: # four of a kind  
            return self.tieBreak(hand2,1) 

        else:   # straight flush and royal flush 
            return self.tieBreak(hand2, 4) 


#---------------------------------------------------------------
# Initial tests 
#---------------------------------------------------------------


# # # # # ----------------------------testing holdEmBestHand----------------
# testcase = [ 
#  # [ [ 'HA' ] , [ ] ] 
#  [ [ 'HA','H2','S5','DK','C9','C7' ] , [ 'HA','S5','DK','C9','C7' ] ] , 
#  [ [ 'HA','H2','S5','DK','C3','C7' ] , [ 'HA','S5','DK','C3','C7' ] ] ,
#  [ [ 'HA','H2','S5','DK','C2','C7' ] , [ 'HA','H2','DK','C2','C7' ] ] ,
#  [ [ 'HA','H2','S5','D5','C2','C7' ] , [ 'HA','H2','D5','C2','S5' ] ] ,
#  [ [ 'HA','H2','S5','D2','C2','C7' ] , [ 'HA','H2','D2','C2','C7' ] ] ,
#  [ [ 'HA','H2','H5','H4','H9','C7' ] , [ 'HA','H2','H5','H4','H9' ] ] ,
#  [ [ 'HA','H2','H5','H4','H9','C7','H3' ] , [ 'HA','H2','H5','H4','H3' ] ] ,
#  [ [ 'HA','H2','H5','H4','H9','C7','D3' ] , [ 'HA','H2','H5','H4','H9' ] ] ,
#  [ [ 'H2','H3','H4','H5','H6','H7', 'H8' ] , [ 'H4','H5','H6','H7', 'H8' ] ] ,
#  [ [ 'HA','H2','H3','H4','H5','H6','H7' ] , [ 'H3','H4','H5','H6','H7' ] ] ,
#  [ [ 'H2', 'C2', 'D2', 'S2', 'HA', 'SA', 'C9' ] , [ 'H2', 'C2', 'D2', 'S2', 'HA' ] ] ,
#  [ [ 'H2', 'C2', 'D2', 'S2', 'HA', 'SA', 'CA' ] , [ 'H2', 'C2', 'D2', 'S2', 'CA' ] ] ,
#  [ [ 'H9', 'HK', 'HQ', 'HJ', 'HT', 'HA' ] , [ 'HA', 'HK', 'HQ', 'HJ', 'HT',] ] ,
#  [ [ 'H2', 'C2', 'S3', 'C3', 'D4', 'H4', 'HK'  ] , ['S3', 'C3', 'D4', 'H4', 'HK'] ] ,
#  [ [ 'H2', 'C2', 'S3', 'C3', 'D4', 'CK', 'HK'  ] , ['C3','S3', 'D4', 'CK', 'HK'] ] ,
#  [ [ 'H2', 'CT', 'S9', 'C3', 'D4', 'CK', 'HK'  ] , ['HK','CK','CT','S9','D4'] ] ,
#  [ [ 'H2', 'CT', 'S9', 'C3', 'D4', 'CK'  ] , ['C3' , 'CK','CT','S9','D4'] ] ,
#  [ [ 'HA','D2','H3','H4','H5','D6','H7' ] , [ 'HA','H3','H4','H5','H7' ] ] ,
#  [ [ 'HA','H2','H3','H4','H5','D6','H7' ] , [ 'HA','H3','H4','H5','H2' ] ] ,
#  [ [ 'H2','D2','H3','H4','H5','D6','H6' ] , [ 'D2','H3','H4','H5','D6', ] ] ,
# ]
# 
# count = 0 
# for test in testcase: 
#     hand1 = hand( [card(l) for l in test[0] ] ) 
#     hand2 = hand( [card(l) for l in test[1] ] )
# 
#     temp1 = hand1.holdEmBestHand().rank_list; temp1.sort() 
#     temp2 = hand2.rank_list; temp2.sort()
#     if not( temp1 == temp2 ):
#         print( 'Hand 1: ' , hand1 ) 
#         print( 'best hand:' , hand1.holdEmBestHand() )
#         print( 'Expected: ' , hand2 ) 
# 
#         quit() 
#     count += 1 
# 
# print( 'Finished {} test cases for holdEmBestHand() '.format(count)  ) 


# # # # #-----------------------------testing isBetter ------------------------------
# testcase= [ 
#  [ False, [ 'H3', 'D5', 'S6', 'C9', 'D2'],  [ 'H3', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ False, [ 'H3', 'D5', 'S6', 'C9', 'D2'],  [ 'H3', 'D5', 'S6', 'C9', 'D3']   ],  
#  [ True , [ 'H3', 'D5', 'S6', 'C9', 'D3'],  [ 'H3', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ True , [ 'H4', 'D5', 'S6', 'C9', 'D3'],  [ 'H4', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ True , [ 'H4', 'D5', 'S6', 'CA', 'D3'],  [ 'H4', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ False, [ 'H4', 'D5', 'S6', 'CA', 'D3'],  [ 'H2', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ True , [ 'H4', 'D5', 'S6', 'C4', 'D3'],  [ 'H2', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ True , [ 'H4', 'D5', 'S3', 'C4', 'D3'],  [ 'H9', 'D5', 'S6', 'C9', 'D2']   ],  
#  [ True , [ 'H4', 'D5', 'S3', 'C3', 'D3'],  [ 'H9', 'D6', 'S6', 'C9', 'D2']   ],  
#  [ False, [ 'H4', 'D5', 'S3', 'C3', 'D3'],  [ 'H3', 'D3', 'S3', 'CA', 'D2']   ],  
#  [ False, [ 'H4', 'D5', 'S3', 'C3', 'D3'],  [ 'H3', 'D3', 'S3', 'CJ', 'D2']   ],  
#  [ False, [ 'H4', 'D5', 'S3', 'C3', 'D3'],  [ 'H3', 'D3', 'S3', 'C8', 'D2']   ],  
#  [ True , [ 'H4', 'D4', 'S3', 'C3', 'D3'],  [ 'H3', 'D3', 'S3', 'C8', 'D2']   ],  
#  [ True , [ 'H4', 'HJ', 'H3', 'H6', 'H5'],  [ 'H3', 'D4', 'S5', 'C6', 'D7']   ],  
#  [ False, [ 'H3', 'D3', 'S3', 'C8', 'D2'],  [ 'H3', 'D4', 'S5', 'C6', 'D7']   ],  
#  [ False, [ 'H3', 'D3', 'S3', 'C3', 'D2'],  [ 'H3', 'H4', 'H5', 'H6', 'H7']   ],  
#  [ True , [ 'H3', 'D3', 'S3', 'C3', 'D2'],  [ 'H3', 'H4', 'H5', 'H6', 'C7']   ],  
#  [ True , [ 'HT', 'CJ', 'SQ', 'CK', 'DA'],  [ 'H3', 'H4', 'H5', 'H6', 'CA']   ],  
#  [ True , [ 'HA', 'S5','DK','C2','C7' ] ,   [ 'HA','H3','DK','C2','C7' ]      ] , 
# ]
# 
# 
# count = 0 
# for test in testcase: 
#     hand1 = hand( [card(l) for l in test[1] ] ) 
#     hand2 = hand( [card(l) for l in test[2] ] ) 
#     if not( test[0] == hand1.isBetter(hand2) ): 
#         print( 'Hand 1: ' , hand1 ) 
#         print( 'Hand 2: ' , hand2 ) 
#         quit() 
#     count += 1 
# 
# print( 'Finished {} test cases for isBetter '.format(count)  ) 

# mycard = card( 'HA') 
# # print( mycard.suit ) 
# # print( mycard.rank ) 
# 
# card_list = [] 
# # for j in range(5): 
# #     card_list.append( card.get_random()  ) 
# #     print( card_list[-1]  ) 
# 
# 
# myhand = hand( card_list ) 
# # random flush 
# myhand = hand( [card('H'+rand.choice([str(num) for num in range(2,10)] + ['T','J','Q','K','A'] ) )  for j in range(5) ] ) 
# # random straight  
# tmp = rand.choice( [j for j in range(2,11) ] ) - 2  
# myhand = hand( [ card(rand.choice(card.suits)+card.ranks[tmp+j]  ) for j in range(5)  ] ) 
# 
# # # check ace as low
# # tmp = 0 
# # tmplist = [ card(rand.choice(card.suits)+card.ranks[tmp+j]  ) for j in range(4)  ]
# # tmplist.append( card('HA')  ) 
# # myhand = hand( tmplist ) 
# 
# # straight flush 
# 
# 
# # n of a kind
# str_list = [ 'HA', 'DK', 'SK', 'CK', 'HT' ]  # three of a kind
# str_list = [ 'HA', 'DK', 'SK', 'CK', 'DA' ]  # full house 
# myhand = hand( [ card(l) for l in str_list  ] )


# # # # modify hand ----------------------------------------------------
# myhand = hand( [] ) 
# print( myhand ) 
# myhand.addCard( card.get_random() ) 
# myhand.addCard( card.get_random() ) 
# print( myhand ) 
# print( myhand.card_list ) 
# print( myhand.rank_list ) 
# 
# myhand.addCard( card('HA') ) 
# myhand.addCard( card('HA') ) 
# myhand.addCard( card('CA') ) 
# myhand.addCard( card('DA') ) 
# print(myhand.rank_list) 
# myhand.removeCard( card('HA') ) 
# print(myhand.rank_list) 
# print(myhand.handRank() ) 
# 
# print( myhand ) 
# print( 'Is duplicate? ', myhand.isDuplicate() ) 
# 
# 
# 
# str_list = [ 'HA', 'DK', 'SK', 'CK', 'DA', 'D2', 'H5' ]  # full house 
# myhand = hand( [ card(l) for l in str_list  ] )
# 
# 
# 
# myhand.removeCard( card('DA') ) 
# print( '\n\n\n' ) 
# print( 'Hand (original)', myhand ) 
# besthand = myhand.holdEmBestHand()
# print( 'Hand: ', myhand) 
# print( 'Ranking of hand: ', besthand.handRank()  ) 
# print( 'corresponding hand:' , besthand ) 

# # # # random best of 7 card hand-------------------------------------------------

# 10**3 is decent, especially for the speed.   
# for n in [10,100,1000,10**4, 10**5]: 
# for n in [5000]: 
# 
#     count_list = [0]*10
#     for j in range(n): 
#     
#         card_list = [] 
#         while len(card_list) < 7: 
#             newCard = card.get_random() 
#             if not newCard in card_list: 
#                 card_list.append( newCard ) 
#         
#         myhand = hand( card_list ) 
#         besthand = myhand.holdEmBestHand() 
#         
#         # print( '-------------\n', myhand , '\n' ) 
#         # print( 'Check Royal Flush   :' , myhand.isRoyalFlush() )  
#         # print( 'Check Straight Flush:' , myhand.isStraightFlush() )  
#         # print( 'Check 4 of a kind   :', myhand.isKind(4) )
#         # print( 'Check Full House    :' , myhand.isFullHouse() )  
#         # print( 'Check Flush         :' , myhand.isFlush() )  
#         # print( 'Check Straight      :' , myhand.isStraight() )  
#         # print( 'Check 3 of a kind   :', myhand.isKind(3) )
#         # print( 'Check two pair      :', myhand.isTwoPair()  )
#         # print( 'Check pair          :', myhand.isKind(2) )
#         # 
#         # print( 'Best hand:  ' , besthand ) 
#        
#         count_list[ besthand.handRank() ] += 1 
#     
#     print( '\n---------Results for n={}----------\n'.format(n)  ) 
#     print( 'Royal Flush   : {:8d}, Prob: {:8.6f}'.format( count_list[9], count_list[9]/n*100 ) ) 
#     print( 'Straight Flush: {:8d}, Prob: {:8.6f}'.format( count_list[8], count_list[8]/n*100 ) ) 
#     print( '4 of a kind   : {:8d}, Prob: {:8.6f}'.format( count_list[7], count_list[7]/n*100 ) ) 
#     print( 'Full House    : {:8d}, Prob: {:8.6f}'.format( count_list[6], count_list[6]/n*100 ) ) 
#     print( 'Flush         : {:8d}, Prob: {:8.6f}'.format( count_list[5], count_list[5]/n*100 ) ) 
#     print( 'Straight      : {:8d}, Prob: {:8.6f}'.format( count_list[4], count_list[4]/n*100 ) ) 
#     print( '3 of a kind   : {:8d}, Prob: {:8.6f}'.format( count_list[3], count_list[3]/n*100 ) ) 
#     print( 'two pair      : {:8d}, Prob: {:8.6f}'.format( count_list[2], count_list[2]/n*100 ) ) 
#     print( 'pair          : {:8d}, Prob: {:8.6f}'.format( count_list[1], count_list[1]/n*100 ) ) 
#     print( 'high card     : {:8d}, Prob: {:8.6f}'.format( count_list[0], count_list[0]/n*100 ) ) 
# 



# # # # random 5 card hand-------------------------------------------------
# # n = 50000000 # matched quite well. 
# n = 5000
# count_list = [0]*10
# for j in range(n): 
# 
#     card_list = [] 
#     while len(card_list) < 5: 
#         newCard = card.get_random() 
#         if not newCard in card_list: 
#             card_list.append( newCard ) 
#     
#     myhand = hand( card_list ) 
#     
#     # print( '-------------\n', myhand , '\n' ) 
#     # print( 'Check Royal Flush   :' , myhand.isRoyalFlush() )  
#     # print( 'Check Straight Flush:' , myhand.isStraightFlush() )  
#     # print( 'Check 4 of a kind   :', myhand.isKind(4) )
#     # print( 'Check Full House    :' , myhand.isFullHouse() )  
#     # print( 'Check Flush         :' , myhand.isFlush() )  
#     # print( 'Check Straight      :' , myhand.isStraight() )  
#     # print( 'Check 3 of a kind   :', myhand.isKind(3) )
#     # print( 'Check two pair      :', myhand.isTwoPair()  )
#     # print( 'Check pair          :', myhand.isKind(2) )
#     # 
#     # print( 'Best hand:  ' , myhand.handRank() ) 
#    
#     count_list[ myhand.handRank() ] += 1 
# 
# print( '\n---------Results----------\n' ) 
# print( 'Royal Flush   : {:8d}, Prob: {:8.6f}'.format( count_list[9], count_list[9]/n*100 ) ) 
# print( 'Straight Flush: {:8d}, Prob: {:8.6f}'.format( count_list[8], count_list[8]/n*100 ) ) 
# print( '4 of a kind   : {:8d}, Prob: {:8.6f}'.format( count_list[7], count_list[7]/n*100 ) ) 
# print( 'Full House    : {:8d}, Prob: {:8.6f}'.format( count_list[6], count_list[6]/n*100 ) ) 
# print( 'Flush         : {:8d}, Prob: {:8.6f}'.format( count_list[5], count_list[5]/n*100 ) ) 
# print( 'Straight      : {:8d}, Prob: {:8.6f}'.format( count_list[4], count_list[4]/n*100 ) ) 
# print( '3 of a kind   : {:8d}, Prob: {:8.6f}'.format( count_list[3], count_list[3]/n*100 ) ) 
# print( 'two pair      : {:8d}, Prob: {:8.6f}'.format( count_list[2], count_list[2]/n*100 ) ) 
# print( 'pair          : {:8d}, Prob: {:8.6f}'.format( count_list[1], count_list[1]/n*100 ) ) 
# print( 'high card     : {:8d}, Prob: {:8.6f}'.format( count_list[0], count_list[0]/n*100 ) ) 



