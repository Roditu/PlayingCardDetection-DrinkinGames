import cv2

def closeState(status):

    

    font_color = (255,255,255)
    close = False

    while True:
        

        mainwin = cv2.imread('asset/grass.jpg')
        mainwin = cv2.resize(mainwin, (853,640))
        key = cv2.waitKey(1)

        if status == 1:
            cv2.putText(mainwin, "P1 Wins !!!", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "Press 'space' to close the game", (30, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color,3)
            cv2.imshow('close', mainwin)
            if key == ord(' '):
                close = True
                break
        elif status == 2:
            cv2.putText(mainwin, "P2 Wins", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "Press 'space' to close the game", (30, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.imshow('close', mainwin)
            if key == ord(' '):
                close = True
                break
        elif status == 3:
            cv2.putText(mainwin, "DRAW", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.putText(mainwin, "Press 'space' to close the game", (30, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 3)
            cv2.imshow('close', mainwin)
            if key == ord(' '):
                close = True
                break

        if close:
            break    
    
    cv2.destroyAllWindows()


