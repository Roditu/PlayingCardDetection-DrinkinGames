import numpy as np
import cv2 
import random
import KlasifikasiCNN as mCNN
import menu
import close

cardName = [
    "Kartu Tutup",      # 0
    "Keriting Dua",     # 1
    "Keriting Tiga",    # 2
    "Keriting Empat",   # 3
    "Keriting Lima",    # 4
    "Keriting Enam",    # 5
    "Keriting Tujuh",   # 6
    "Keriting Delapan", # 7
    "Keriting Sembilan",# 8
    "Keriting Sepuluh", # 9
    "Keriting Jack",    # 10
    "Keriting Queen",   # 11
    "Keriting King",    # 12
    "Keriting Ace",     # 13
    "Hati Dua",         # 14
    "Hati Tiga",        # 15
    "Hati Empat",       # 16
    "Hati Lima",        # 17
    "Hati Enam",        # 18
    "Hati Tujuh",       # 19
    "Hati Delapan",     # 20
    "Hati Sembilan",    # 21
    "Hati Sepuluh",     # 22
    "Hati Jack",        # 23
    "Hati Queen",       # 24
    "Hati King",        # 25
    "Hati Ace",         # 26
    "Wajik Dua",        # 27
    "Wajik Tiga",       # 28
    "Wajik Empat",      # 29
    "Wajik Lima",       # 30
    "Wajik Enam",       # 31
    "Wajik Tujuh",      # 32
    "Wajik Delapan",    # 33
    "Wajik Sembilan",   # 34
    "Wajik Sepuluh",    # 35
    "Wajik Jack",       # 36
    "Wajik Queen",      # 37
    "Wajik King",       # 38
    "Wajik Ace",        # 39
    "Sekop Dua",        # 40
    "Sekop Tiga",       # 41
    "Sekop Empat",      # 42
    "Sekop Lima",       # 43
    "Sekop Enam",       # 44
    "Sekop Tujuh",      # 45
    "Sekop Delapan",    # 46
    "Sekop Sembilan",   # 47
    "Sekop Sepuluh",    # 48
    "Sekop Jack",       # 49
    "Sekop Queen",      # 50
    "Sekop King",       # 51
    "Sekop Ace",        # 52
]

model = mCNN.LoadModel('CardWeight.h5')

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Image Preprocessing
def binerimg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 100, 150)
    kernel = np.ones((3, 3))
    dial = cv2.dilate(canny, kernel=kernel, iterations=1)
    imgThres = cv2.erode(dial, kernel, iterations=1)
    return canny

# Deteksi Contour dan koordinat
def getContours(img, kontur, draw = False):

    contours, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cropped_frames = []
    cardCoor = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        if area > 5000:
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            numCorners = len(approx)

            if numCorners == 4:
                x,y,w,h = cv2.boundingRect(approx)
                cardCoor.append((x,y))

                if draw:
                    cv2.rectangle(kontur, (x,y), (x+w, y+h), (0,255,0), 3)  

                cropped_frame = img[y:y+h, x:x+w]

                cropped_frames.append(cropped_frame)

    for i, cropped_frame in enumerate(cropped_frames):
        cv2.namedWindow(f'Cropped Frame{i}', cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f'Cropped Frame{i}', cropped_frame.shape[1], cropped_frame.shape[0])
        # cv2.imshow(f'Cropped Frame{i}', cropped_frame)
       
    return cropped_frames, cardCoor

# Tipe Kartu
def cardType(card_index):
    if 1<= card_index <= 13:
        return "Keriting"
    elif 14<= card_index <= 26:
        return "Hati"
    elif 27<= card_index <= 39:
        return "Wajik"
    elif 40<= card_index <= 52: 
        return "Sekop"
    else:
        return None

# Membandingkan Kartu Player
def comparedCard(card1, card2):

    value1 = cardName.index(card1)
    value2 = cardName.index(card2)

    type1 = cardType(value1)
    type2 = cardType(value2)

    if type1 is not None and type1 == type2:
        if value1 > value2:
            return 1
        elif value1 < value2:
            return -1
        else:
            return 0
    else:
        return None

# Prediksi Kartu  
def predik(bgr_frames, cardCoor):
    storedCard =[]

    for i, bgr_frame in enumerate(bgr_frames):
        X = []

        img = cv2.resize(bgr_frame, (128, 128))
        img = img.astype('float32') / 255  # Normalize to [0, 1]
        X.append(img)

        X = np.array(X)
        X = X.astype('float32')

        hs = model.predict(X,verbose = 0)
        n = np.max(np.where(hs== hs.max()))

        
 
        cv2.putText(CardRes_bg, f'{cardName[n]}{"{:.2f}".format(hs[0,n])}', cardCoor, cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        storedCard.append(cardName[n])
    
    return storedCard

# Menentukan pemenang dari hasil compare
def decider(storedCard1, storedCard2):
    global turn
    global P1_Cardleft
    global P2_Cardleft
    global debounce_timer
    
    if len(storedCard1) ==1 and len(storedCard2) == 1:
        winner = comparedCard(storedCard1[0], storedCard2[0])
        if winner == 1:
            cv2.putText(frame, f"{storedCard1[0]} wins!", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 1)
            turn = 1
            if debounce_timer <= 0:
                P1_Cardleft = P1_Cardleft - 1
                P2_Cardleft = P2_Cardleft - 1
                debounce_timer = 200
            else:
                debounce_timer -= 1
          
        elif winner == -1:
            cv2.putText(frame, f"{storedCard2[0]} wins!", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 1)
            turn = 2
            if debounce_timer <= 0:
                P1_Cardleft = P1_Cardleft - 1
                P2_Cardleft = P2_Cardleft - 1
                debounce_timer = 200
            else:
                debounce_timer -= 1
            
        else:
            cv2.putText(stat_bg, "Card not Eligible", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, font_color, 1)
            print("Card not eligible")
            print(comparedCard(storedCard1[0], storedCard2[0]))

def border(frame):
    frame = cv2.copyMakeBorder(frame, 3,3,3,3, cv2.BORDER_CONSTANT, (0,0,0))
    return frame

font_color = (255, 255, 255)  # White color in BGR format

# Generate kartu bukaan 
cards_without_tutup = [card for card in cardName if card != "Kartu Tutup"]
randomCard = random.choice(cards_without_tutup)
indexRandomCard = cardName.index(randomCard)
typeRandomCard = cardType(indexRandomCard)

# State Gameplay
turn = 0
P1_Cardleft = 5
P2_Cardleft = 5
debounce_timer = 0

# State Menu
Menu_state = True
Closing_state = 0
status = 0


while True:
    if Menu_state:
        menu.menuState()
        Menu_state = False
    
    ret, frame = cap.read()
    
    # Main Window
    mainwin = cv2.imread('asset/grass.jpg')
    mainwin = cv2.resize(mainwin, (853,640))

    # Window Score(Card Left)
    DisScore_bg = cv2.imread('asset/dirt.jpeg')
    DisScore_bg = cv2.resize(DisScore_bg, (187,154))
    DisScore_bg = border(DisScore_bg)
    cv2.putText(DisScore_bg, "Card Left", (48, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1)
    cv2.putText(DisScore_bg, "P1", (30, 69), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1)
    cv2.putText(DisScore_bg, "P2", (130, 69), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1)
    cv2.putText(DisScore_bg, f"{P1_Cardleft}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 2.5, font_color, 1)
    cv2.putText(DisScore_bg, f"{P2_Cardleft}", (120, 140), cv2.FONT_HERSHEY_SIMPLEX, 2.5, font_color, 1)

    # Window Hasil Deteksi kartu
    CardRes_bg = cv2.imread('asset/dirt.jpeg')
    CardRes_bg = cv2.resize(CardRes_bg, (629,124))
    CardRes_bg = border(CardRes_bg)
    cv2.putText(CardRes_bg, "P1 Card", (110, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1)
    cv2.putText(CardRes_bg, "P2 Card", (440, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1)

    # Window Status
    stat_bg = cv2.imread('asset/dirt.jpeg')
    stat_bg = cv2.resize(stat_bg, (187,284))
    stat_bg = border(stat_bg)

    biner = binerimg(frame)
    kontur = frame.copy()
    height, width, _  = frame.shape
    midPoint = width // 2
    cv2.line(frame, (midPoint,0), (midPoint, height), (0,204,0), 5)

    # Membagi Side Player
    p1side = biner[:, :midPoint]
    p2side = biner[:, midPoint:]
    # cv2.imshow('p1side', p1side)
    # cv2.imshow('p2side', p2side)
    
    # Deteksi Contour tiap Side
    cropped_frames1, cardCoor1 = getContours(p1side, kontur, draw=True)
    cropped_frames2, cardCoor2 = getContours(p2side, kontur, draw=True)

    # Mengubah format biner(gray) ke BGR
    bgr_frames1 = [cv2.cvtColor(cropped_frame, cv2.COLOR_GRAY2BGR) for cropped_frame in cropped_frames1]
    bgr_frames2 = [cv2.cvtColor(cropped_frame, cv2.COLOR_GRAY2BGR) for cropped_frame in cropped_frames2]
    # for i, bgr_frame in enumerate(bgr_frames1):
    #    cv2.namedWindow(f'BGR Frame {i}', cv2.WINDOW_NORMAL)
    #    cv2.resizeWindow(f'BGR Frame {i}', bgr_frame.shape[1], bgr_frame.shape[0])
    #    cv2.imshow(f'BGR Frame {i}', bgr_frame)

    # cv2.imshow('biner', biner)
    
    # cv2.imshow('contur', kontur)

    font_color = (255, 255, 255)  # White color in BGR format

    storedCard1 = predik(bgr_frames1, (60, 60))
    storedCard2 = predik(bgr_frames2, (370, 60))

    ## POSISI TURN
    if turn == 1:
        print("Player 1 Move First")
        cv2.putText(stat_bg, "Player 1 Move First", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        if storedCard2  and not storedCard1:
            cv2.putText(stat_bg, "Its not your turn", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        else :
            decider(storedCard1, storedCard2)
    elif turn == 2:
        cv2.putText(stat_bg, "Player 2 Move First", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        if storedCard1 and not storedCard2:
            cv2.putText(stat_bg, "Its not your turn", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
        else :
            decider(storedCard1, storedCard2)
    elif turn == 0:
        cv2.putText(frame, "Dealer Card", (253, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 1, cv2.LINE_4)
        cv2.putText(frame, f"{randomCard}", (255, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1, cv2.LINE_4)
        if storedCard1 and storedCard2:
            iCardP1 = cardName.index(storedCard1[0])
            # print("value 1 =", value1)
            iCardP2 = cardName.index(storedCard2[0])
            # print("value 2 =" , value2)

            type1 = cardType(iCardP1)
            # print("type 1= "+ type1)
            type2 = cardType(iCardP2)
            # print("type 2=" + type2)
            if iCardP1 or iCardP2 == indexRandomCard:
                print("That card is a Dealer card")
                print("Please Draw Another Card")

            if type1 == type2 == typeRandomCard:
                if iCardP1 > iCardP2:
                    print("Player 1 Win")
                    cv2.putText(stat_bg, "Player 1 Win", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
                    cv2.putText(frame, "Player 1 Win", (230, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
                    turn = 1
                    if debounce_timer <= 0:
                        P1_Cardleft = P1_Cardleft - 1
                        P2_Cardleft = P2_Cardleft - 1
                        debounce_timer = 200
                    else:
                        debounce_timer -= 1
        
                elif iCardP1 < iCardP2:
                    print("Player 2 Win")
                    cv2.putText(stat_bg, "Player 2 Win", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
                    cv2.putText(frame, "Player 2 Win", (230, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
                    turn = 2
                    if debounce_timer <= 0:
                        P1_Cardleft = P1_Cardleft - 1
                        P2_Cardleft = P2_Cardleft - 1
                        debounce_timer = 200
                    else:
                        debounce_timer -= 1
                  
                else:
                    print("Something Wrong")
            else:
                print("Card not Eligible")
    
    # Status Draw
    if storedCard1: 
        if storedCard1[0]== "Kartu Tutup":
            print("Player 1, please draw a Card")
            cv2.putText(stat_bg, "Player 1, please draw a Card", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
            if debounce_timer <= 0:
                P1_Cardleft = P1_Cardleft + 1
                debounce_timer = 200
            else:
                debounce_timer -= 1
    elif storedCard2: 
        if storedCard2[0]== "Kartu Tutup":
            print("Player 2, please draw a Card")
            cv2.putText(stat_bg, "Player 2, please draw a Card", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
            if debounce_timer <= 0:
                P2_Cardleft = P2_Cardleft + 1
                debounce_timer = 200
            else:
                debounce_timer -= 1

    # Win Condition
    if P1_Cardleft == 0:
        print("Player 1 Win!")
        Closing_state = 1
        status = 1
    elif P2_Cardleft == 0:
        print("Player 2 Win!")
        Closing_state = 1
        status = 2
    elif P1_Cardleft == 0 and P2_Cardleft == 0:
        print("Draw")
        Closing_state = 1
        status = 3  

    if debounce_timer > 0:
        debounce_timer -= 1

    # Mengatur Window
    cv2.putText(stat_bg, f"scan after = {debounce_timer}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, font_color, 1)
    cv2.imshow('asli', frame)
    mainwin[0 : frame.shape[0],0 : frame.shape[1]] = frame
    mainwin[10: 170, 650: 843] = DisScore_bg
    mainwin[490: 620, 5: 640] = CardRes_bg
    mainwin[190: 480, 650: 843] = stat_bg
    cv2.imshow("Main",mainwin)
    
    print(f'timer = {debounce_timer}')
    
    # print(f'P1_Cardleft = {P1_Cardleft} & P2_Cardleft = {P2_Cardleft}')

    if Closing_state == 1:
        close.closeState(status)
        Closing_state = 2

    if (cv2.waitKey(1) == ord('q')) or (Closing_state == 2):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()