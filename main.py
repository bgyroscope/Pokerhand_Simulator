# 2021.12.31 
 
import numpy as np 
import random as rand 
import card_hand_module as ch


# Go to line 120 to edit relavant parameters 

# find the odds of winning 
def find_odds( pocket, table, n ): 
    ''' find the odds of win given pocket card and table cards expressed as list ''' 
    pocket_hand = ch.hand( [ ch.card(s) for s in pocket]  ) 
    
    win = 0 
    for j in range(n) : 
        # add random until table has 5 cards 
        table_hand = ch.hand( [ ch.card(s) for s in table ] )
        while len( table_hand.card_list ) < 5: 
            c = ch.card.get_random() 
            if not( c in pocket_hand.card_list ) and not(c in table_hand.card_list): 
                table_hand.addCard(c) 
    
        # get random opponent pocket 
        opp_pocket = ch.hand( [ ]  ) 
        while len( opp_pocket.card_list ) < 2: 
            c = ch.card.get_random() 
            if not( c in pocket_hand.card_list ) and not(c in table_hand.card_list) and not( c in opp_pocket.card_list ): 
                opp_pocket.addCard(c) 
    
    
        myhand = pocket_hand.copy() 
        opphand= opp_pocket.copy() 
    
        for c in table_hand.card_list: 
            myhand.addCard( c ) 
            opphand.addCard( c ) 
    
        # print( '\n----------\n') 
        # print( myhand ) 
        # print( opphand )
        
    
        # find best hand 
        myhand = myhand.holdEmBestHand() 
        opphand = opphand.holdEmBestHand() 
    
        if myhand.isBetter( opphand ) : 
            # print( 'win' ) 
            win += 1 

    return  win / n    


# find the odds of winning 
def find_odds2( pocket, table, n, nplay ): 
    ''' find the odds of win given pocket card and table cards expressed as list ''' 
    # Nplay is the number of other players 
    pocket_hand = ch.hand( [ ch.card(s) for s in pocket]  ) 
    
    win = 0 
    for j in range(n) : 
        # add random until table has 5 cards 
        table_hand = ch.hand( [ ch.card(s) for s in table ] )
        while len( table_hand.card_list ) < 5: 
            c = ch.card.get_random() 
            if not( c in pocket_hand.card_list ) and not(c in table_hand.card_list): 
                table_hand.addCard(c) 
   

        # list of all cards 
        allcards = table_hand.copy() 
        for c in pocket_hand.card_list: 
            allcards.addCard( c ) 

        opp_hands = [ ]

        for k in range(nplay) : 
            # get random opponent pocket 
            opp_pocket = ch.hand( [ ]  ) 
            while len( opp_pocket.card_list ) < 2: 
                c = ch.card.get_random() 
                if not( c in allcards.card_list ): 
                    opp_pocket.addCard(c) 
                    allcards.addCard(c) 
    
            opp_hands.append( opp_pocket  ) 

        myhand = pocket_hand.copy() 
        opphand= opp_pocket.copy() 
    
        for c in table_hand.card_list: 
            myhand.addCard( c ) 
        
        for c in table_hand.card_list: 
            for k in range(nplay): 
                opp_hands[k].addCard( c ) 
    
        # print( '\n----------\n') 
    
        # find best hand 
        # print('Before: ', myhand ) 
        myhand = myhand.holdEmBestHand() 
        # print( myhand ) 

        for k in range(nplay): 
            # print('Before: ',  opp_hands[k] ) 
            opp_hands[k] = opp_hands[k].holdEmBestHand() 
            # print( opp_hands[k] ) 

        if sum( [ myhand.isBetter( h ) for h in opp_hands] ) == nplay : 
            # print( 'win' ) 
            win += 1 

    return  win / n    



# # edit parameters here 
n = 1000  # simulations to do 

# get input...
# recall h,s,d,c for suit, 2-9, T,J,Q,K,A for rank  
nplay =       3;  # other players  
pocket_str ='h9, hT   ';  
table_str  =' hJ, hQ, hK, hA, d8  '; 

pocket_str = pocket_str.upper() 
pocket_str = pocket_str.replace(' ','') 

table_str = table_str.upper() 
table_str = table_str.replace(' ','') 


# pocket = [  'DQ', 'C7'   ] 
pocket = pocket_str.split(',') 
# table =  [    'D2', 'C2', 'HK'  ] 
if table_str == '': 
    table = [] 
else: 
    table = table_str.split(',') 

print( nplay, 'other players' ) 
print( "Pocket: ", pocket ) 
print( "Table:  ", table ) 

# # # calculate odds from input 
# p = find_odds( pocket, table, n)
p = find_odds2( pocket, table, n, nplay)
print( 'Prob of win {:6.4f} '.format( p  )  ) 
# print( 'win to loss ratio of {:6.4f} needed.'.format( (1-p)/p ) , ' (bet * ratio >= pot?)' )  




# # # for calculating pocket probabilities 
# ranks = [ str(i) for i in range(2,10) ]  + [ 'T', 'J', 'Q', 'K', 'A' ]  
# # ranks = [ '2', '3', 'A' ]  
# 
# out_arr = np.zeros( (len(ranks), len(ranks) )  ) 
# 
# for k, r1 in enumerate( ranks ) : 
#     # print( '---------------------' ) 
#     for l,r2 in enumerate(ranks[k:] ): 
#         pocket = [ 'H{}'.format( r1 ) , 'H{}'.format(r2) ] 
# 
#         if pocket[0] == pocket[1] : 
#             continue
#         else: 
#             # print( pocket ) 
# 
# 
#             # print( '{},{}  Prob of win: {:6.4f}'.format(pocket[0],pocket[1], find_odds(pocket,table,n)  ) ) 
#             out_arr[ k, l+k ]  = find_odds( pocket, table, n ) 
#             out_arr[ l+k, k ]  = out_arr[k,l+k] 
#             # print( k, l+k, out_arr[k,l+k]  ) 
# 
# 
# print( out_arr ) 
# 
# np.savetxt( 'output.csv', out_arr, delimiter=',', header=','.join(ranks)  ) 
# 
# quit() 




