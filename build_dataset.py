import cv2
import os
import datetime
import time
import numpy as np

# Untuk penamaan semua class di Model ML
cardName = [
    "Kartu Tutup",
    "Keriting Dua",
    "Keriting Tiga",
    "Keriting Empat",
    "Keriting Lima",
    "Keriting Enam",
    "Keriting Tujuh",
    "Keriting Delapan",
    "Keriting Sembilan",
    "Keriting Sepuluh",
    "Keriting Jack",
    "Keriting Queen",
    "Keriting King",
    "Keriting Ace",
    "Hati Dua",
    "Hati Tiga",
    "Hati Empat",
    "Hati Lima",
    "Hati Enam",
    "Hati Tujuh",
    "Hati Delapan",
    "Hati Sembilan",
    "Hati Sepuluh",
    "Hati Jack",
    "Hati Queen",
    "Hati King",
    "Hati Ace",
    "Wajik Dua",
    "Wajik Tiga",
    "Wajik Empat",
    "Wajik Lima",
    "Wajik Enam",
    "Wajik Tujuh",
    "Wajik Delapan",
    "Wajik Sembilan",
    "Wajik Sepuluh",
    "Wajik Jack",
    "Wajik Queen",
    "Wajik King",
    "Wajik Ace",
    "Sekop Dua",
    "Sekop Tiga",
    "Sekop Empat",
    "Sekop Lima",
    "Sekop Enam",
    "Sekop Tujuh",
    "Sekop Delapan",
    "Sekop Sembilan",
    "Sekop Sepuluh",
    "Sekop Jack",
    "Sekop Queen",
    "Sekop King",
    "Sekop Ace",
]

# Kita mulai dari index 0
cardNameIndex = 0

# Fungsi dari pak Akok buat penamaan file menurut waktu diambil
def GetFileName():
    x = datetime.datetime.now()
    s = x.strftime('%Y-%m-%d-%H%M%S%f')
    return s

# Fungsi dari ChatGPT buat menentukan luas area dari 4 titik
def polygon_area(points):
    # 'points' adalah input berupa array yg berisikan 4 titik koordinat kartu
    points = np.vstack((points, points[0]))
    area = 0.5 * np.abs(np.dot(points[:, 0], np.roll(points[:, 1], 1)) - np.dot(points[:, 1], np.roll(points[:, 0], 1)))
    return area

# Fungsi dari pak Akok
def CreateDir(path):
    ls = []
    head_tail = os.path.split(path)
    ls.append(path)
    while len(head_tail[1])>0:
        head_tail = os.path.split(path)
        path = head_tail[0]
        ls.append(path)
        head_tail = os.path.split(path)
    for i in range(len(ls)-2,-1,-1):
        sf = ls[i]
        isExist = os.path.exists(sf)
        if not isExist:
            os.makedirs(sf)

# Fungsi dari pak Akok juga, tapi harus kita modif
def CreateDataSet(sDirektoriData,sKelas,NoKamera,FrameRate):
    global cardName, cardNameIndex

    # For webcam input:
    cap = cv2.VideoCapture(NoKamera)
    TimeStart = time.time()

    # Mengetahui limit detik dalam pengambilan gambar
    saveTimeLimit = time.time()

    # Status record
    isSaving = False
    while cap.isOpened():
        success, frame = cap.read()
        
        # Buat dulu folder sesuai dengan datasetnya
        sDirektoriKelas = sDirektoriData+"/"+cardName[cardNameIndex]
        CreateDir(sDirektoriKelas)

        if not success:
            print("Ignoring empty camera frame.")
            continue

        isDetected = False

        # Image processing
        # ======= 1. ======= Pertama, gambar kita buat grayscale dulu
        # imGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                                                                    
        # imThres = cv2.adaptiveThreshold(imGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,71,10)
        # cv2.imshow("2. Adaptive thres", imThres)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 100, 150)
        kernel = np.ones((3, 3))
        dial = cv2.dilate(canny, kernel=kernel, iterations=1)
        imThres = cv2.erode(dial, kernel, iterations=1)
        cv2.imshow("2. Threshold", canny)


        # ======= 3. ======= Next, kita ambil component yg connected.
        # https://drive.google.com/file/d/1nuPMCajNSBYXBYO4t5nESIi74eNIzb1b/view
        totalLabels, label_ids, values, centroid = cv2.connectedComponentsWithStats(canny, 4, cv2.CV_32S)
        bigIndex = []
        for i in range(totalLabels):
            hw = values[i,2:4]
            if (70<hw[0]<200 and 150<hw[1]<300):
                bigIndex.append(i)

        # ======= 4. ======= Check, apakah ada connected component yg sesuai dengan luas yg kita define
        # Kalo ada kita kotakin
        for i in bigIndex:
            topLeft = values[i,0:2]
            bottomRight = values[i,0:2]+values[i,2:4]
            frame = cv2.rectangle(frame, topLeft, bottomRight, color=(0,0,255), thickness=3)
            # Disini ada break, yg berarti kita cuma ngambil 1 item doang
            break
        # Trus tampilin
        cv2.imshow("4. Hasil habis dikotakin", frame)
        
        # ======= 5. ======= Kita crop yg dikotakin tadi
        for i in bigIndex:
            topLeft = values[i,0:2]
            bottomRight = values[i,0:2]+values[i,2:4]
            cardImage = canny[topLeft[1]:bottomRight[1],topLeft[0]:bottomRight[0]]
            cv2.imshow('5. Hasil dari cardImage', cardImage)
            break
        
        # ======= 6. ======= Ini buat ngerecord datasetnya.
        # Diambil juga dari modul bapaknya, yg dimodif dikit
        TimeNow = time.time()
        if TimeNow-TimeStart>1/FrameRate:
            sfFile = sDirektoriKelas+"/"+GetFileName()
            if isSaving and len(bigIndex) > 0:
                cv2.imwrite(sfFile+'.jpg', cardImage)
            TimeStart = TimeNow

       
        cv2.putText(frame, "Nama Kartu yg direkam:", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"{cardNameIndex+1}. " + cardName[cardNameIndex], (0, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, "Tekan spasi untuk mulai record", (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0,0), 2)
        
       
        if isSaving:
            cv2.putText(frame, "Record", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            saveTimeLimit = time.time()

        cv2.imshow("Tampilan akhir", frame)
        
        key = cv2.waitKey(5)

        # Trigger tekan spasi untuk mulai menyimpan gambar
        if key == 32:
            isSaving = not isSaving

        # Kalo udah lebih dari 5 detik, penyimpanan foto selesai
        if time.time() - saveTimeLimit >= 8:
            cardNameIndex += 1
            isSaving = False

        if key & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

DirektoriDataSet = "dataset"

CreateDataSet(DirektoriDataSet, " ", NoKamera=1, FrameRate=20)