import cv2

def menuState():
    menu_state = 0
    howto_state = 1
    credit_state = 2
    game_state = 3

    current_state = menu_state

    font_color = (0,51,25)

    while True:
        

        mainwin = cv2.imread('asset/grass.jpg')
        mainwin = cv2.resize(mainwin, (853,640))
    


        if current_state == menu_state:
            cv2.putText(mainwin, "Press 'a' to start the game", (20,280), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "Press 's' to see How to Play", (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "Press 'd' to Credit", (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.imshow('menu', mainwin)

            key = cv2.waitKey(1)
            if key == ord('a'):
                current_state = game_state
                break
            elif key == ord('s'):
                current_state = howto_state
            elif key == ord('d'):
                current_state = credit_state

        elif current_state == howto_state:
            cv2.putText(mainwin, "- Draw 5 Cards for each player", (20,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "- First round, Put both player card same as dealer card type", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "- The player who puts the biggest value wins,", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "get the first chance to put a card first", (20, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "in the next Round ", (20, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "- Player who got first move can put cards up to player,", (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "the oppenent move after him", (20, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "Opponent Card have to be the same type", (20, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "- If player doesnt have a same card type,", (20, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "draw a card with showing back side of card", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "- The card player who runs out first wins", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2)
            cv2.putText(mainwin, "Press 'b' to back", (20, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            cv2.imshow('menu', mainwin)
            key = cv2.waitKey(1)
            if key == ord('b'):
                current_state = menu_state
        
        elif current_state == credit_state:
            cv2.putText(mainwin, "M. RADHITO BIL ATHO", (20,280), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "COMPUTER ENGINEERING", (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "INSTITUE OF TECHNOLOGY SEPULUH NOPEMBER", (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 3)
            cv2.putText(mainwin, "Press 'b' to back", (20, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            cv2.imshow('menu', mainwin)
            key = cv2.waitKey(1)
            if key == ord('b'):
                current_state = menu_state 
        
        if current_state == game_state:
            break

    cv2.destroyAllWindows()


