# import pygame
import random
import time
import os
from treys import * # Card, Deck, Evaluator
import holdem_calc as holdem
import copy


# betting function for player
def player_betting(money, min, ai_money, betting_round): 
    if money == 0 or ai_money == 0:
        return 0
    player_bet_amount = -2
    while player_bet_amount < min or player_bet_amount > money:
        player_bet_amount = int(input("How much would you like to bet? " + str(min) + " - " 
        + str(money) + ".\n If you would like to check, enter 0. \n If you would like to fold," +
        " enter -1. (If you enter more than the money that the AI has, your betting amount will" +
        " change to the amount that the AI has.)\n"))
        if (player_bet_amount == -1):
            print("Player folds.\n")
            return -1
        elif player_bet_amount < min or player_bet_amount > money:
            print("Invalid input. Try again.")
        
    if (player_bet_amount > ai_money):
        player_bet_amount  = ai_money
    print("Betting: " + str(player_bet_amount))
    return player_bet_amount

# betting function for the AI
# the money refers to the amount of money the AI has.
# min refers to the minimum amount of money that the AI has to bet. 
# everything else is self explanatory
def ai_betting(money, min, table, ai_hand, player_money, betting_round):
    win_and_tie = 0
    board = copy.deepcopy(table)
    ai = copy.deepcopy(ai_hand)
    if money == 0:
        return 0
    if len(table) == 0:
        win_and_tie = .5
    else: 
        for x in range(len(table)):
            board[x] = Card.int_to_str(board[x])
        for x in range(len(ai_hand)):
            ai[x] = Card.int_to_str(ai[x])
        probability = holdem.calculate(board, True, 1, None, ai + ["?","?"], False)
        win_and_tie = probability[0] + probability[1]
    ai_bet_amount = 0
    rand = random.random()
    if (win_and_tie < .15):
        return -1
    elif (win_and_tie >= .7):
        if (player_money * 2 < money):
            if rand > .25:
                return player_money
        ai_bet_amount  = (int)(money * win_and_tie* rand * (1 + (betting_round)/10))
        if (ai_bet_amount >= money):
            return money
        elif (ai_bet_amount >= player_money):
            return player_money
        elif (ai_bet_amount <= min):
            return min
        return ai_bet_amount
    else: 
        random_mult = random.random()
        if win_and_tie < .3:
            random_mult /= 5
        elif win_and_tie < .5:
            random_mult /= 4
        else: 
            random_mult /= 2
        ai_bet_amount  = (int)(money * win_and_tie* rand * random_mult * (1 + (betting_round)/10))
        if (ai_bet_amount < min):
            if win_and_tie < .5:
                return -1
            else:
                return min
        elif (ai_bet_amount >= player_money and ai_bet_amount <= money):
            return player_money
        elif (ai_bet_amount >= money):
            return money
        return ai_bet_amount

os.system("cls")
player_money = 100
ai_money = 100
evaluator = Evaluator()
while (player_money > 0) and (ai_money > 0):
    player_fold = False
    ai_fold = False
    player_won = False
    player_score = 0
    ai_score = 0  
    pot = 0
    min = 0
    bets_equal = False
    player_bet = 0
    ai_bet = 0
    player_bet_total = 0
    ai_bet_total = 0
    ai_hand = []
    #as long as neither bot or player folds, then the game continues
    while(not player_fold and not ai_fold):
        pot += 2
        ai_money -= 1
        player_money -= 1
       
        betting_round  = 0
        #if turn is True, then the ai bot goes first, if turn is false, then the player decides to bet first
        turn = True
        if  random.random() < 0.5:
            turn  = False
        if(turn):
            deck = Deck() # creates new deck

            ai_hand = deck.draw(2) # deals AI's hand 
            player_hand = deck.draw(2) # deals player's hand
            print("\nYour Cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            table = []
            # 1st round of betting
            betting_round = 1
            while(not bets_equal):
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total 
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                if ai_bet_total == player_bet_total and ai_bet_total != 0:
                    break
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else: 
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                min = player_bet_total - ai_bet_total
                bets_equal = (player_bet_total == ai_bet_total)
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")
            


            table = deck.draw(3) # deals first 3 cards on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            
            # 2nd round of betting
            betting_round = 2
            while(not bets_equal):
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total 
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                if ai_bet_total == player_bet_total and ai_bet_total != 0:
                    break
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else: 
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                min = player_bet_total - ai_bet_total
                bets_equal = (player_bet_total == ai_bet_total)
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")
            

            table += deck.draw(1) # deals 4th card on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            # 3rd round of betting
            betting_round = 3
            while(not bets_equal):
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total 
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                if ai_bet_total == player_bet_total and ai_bet_total != 0:
                    break
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else: 
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                min = player_bet_total - ai_bet_total
                bets_equal = (player_bet_total == ai_bet_total)
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")

            
            table += deck.draw(1) # deals 5th card on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            # 4th round of betting
            betting_round = 4
            while(not bets_equal):
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total 
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                if ai_bet_total == player_bet_total and ai_bet_total != 0:
                    break
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else: 
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                min = player_bet_total - ai_bet_total
                bets_equal = (player_bet_total == ai_bet_total)
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")
            

            player_score = evaluator.evaluate(table, player_hand)
            ai_score = evaluator.evaluate(table, ai_hand)
            break
        else: 
            deck = Deck() # creates new deck

            player_hand = deck.draw(2) # deals player's hand
            ai_hand = deck.draw(2) # deals AI's hand  
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            table = []
            # 1st round of betting
            betting_round = 1
            while(not bets_equal):
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else:
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                if ai_bet_total == player_bet_total and player_bet_total != 0:
                    break
                min = player_bet_total - ai_bet_total
                print(min)
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                
                bets_equal = player_bet_total == ai_bet_total
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")

            
            table = deck.draw(3) # deals first 3 cards on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            # 2nd round of betting
            betting_round = 2
            while(not bets_equal):
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else:
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                if ai_bet_total == player_bet_total and player_bet_total != 0:
                    break
                min = player_bet_total - ai_bet_total
                print(min)
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                
                bets_equal = player_bet_total == ai_bet_total
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")

            

            table += deck.draw(1) # deals 4th card on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            # 3rd round of betting
            betting_round = 3
            while(not bets_equal):
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else:
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                if ai_bet_total == player_bet_total and player_bet_total != 0:
                    break
                min = player_bet_total - ai_bet_total
                print(min)
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                
                bets_equal = player_bet_total == ai_bet_total
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")


            table += deck.draw(1) # deals 5th card on the table
            print("The cards on the table are:")
            Card.print_pretty_cards(table)
            print("\nYour cards are: ")
            Card.print_pretty_cards(player_hand) #prints player's cards with formatting
            # 4th round of betting
            betting_round = 4
            while(not bets_equal):
                player_bet = player_betting(player_money - player_bet_total, min, ai_money+ai_bet_total,betting_round)
                if(player_bet == -1):
                    player_fold = True
                    ai_money += player_bet_total + pot
                    player_money -= player_bet_total
                    print("You fold! AI wins $" + str(pot + player_bet_total))
                    break
                else:
                    player_bet_total += player_bet
                print("Your total bet: " + str(player_bet_total))
                if ai_bet_total == player_bet_total and player_bet_total != 0:
                    break
                min = player_bet_total - ai_bet_total
                print(min)
                print("AI is thinking...")
                ai_bet = ai_betting(ai_money - ai_bet_total, min, table, ai_hand, player_money-player_bet_total, betting_round)
                if(ai_bet == -1):
                    ai_fold = True
                    player_money += ai_bet_total + pot
                    ai_money -= ai_bet_total
                    print("AI folds! You win $" + str(pot + ai_bet_total))
                    break
                else:
                    ai_bet_total += ai_bet
                print("Total AI bet: " + str(ai_bet_total))
                min = ai_bet_total - player_bet_total
                
                bets_equal = player_bet_total == ai_bet_total
            if (ai_fold or player_fold):
                break
            pot += player_bet_total + ai_bet_total
            player_money -= player_bet_total
            ai_money -= ai_bet_total
            player_bet =  0
            ai_bet = 0
            player_bet_total = 0
            ai_bet_total = 0
            print("You have $" + str(player_money))
            print("AI has $" + str(ai_money))
            bets_equal = False
            min = 0
            if player_money == 0 or ai_money == 0:
                input("Press enter to continue...")


            player_score = evaluator.evaluate(table, player_hand)
            ai_score = evaluator.evaluate(table, ai_hand)
            break
    print("\nThe AI's cards were: ")
    Card.print_pretty_cards(ai_hand) #prints AI's cards with formatting
    print("The table cards were: ")
    Card.print_pretty_cards(table)
    if(not player_fold and not ai_fold):
        if player_score < ai_score:
            print("You won  $" + str(pot))
            player_money += pot
        elif player_score == ai_score:
            print("You tied and split the pot!")
            player_money += int(pot/2)
            ai_money += int(pot/2)
        else:
            print("You lost the round! The AI won $" + str(pot))
            ai_money += pot
    input("Press enter to continue...")
    os.system("cls")
    pot = 0
if player_money == 0:
    print("You lost! AI prevails!")
elif ai_money == 0:
    print("You won the game! Humans prevail!")

    