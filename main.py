import cv2
import pafy
import numpy as np
import winsound # Demo: segnale sonoro
url = "https://www.youtube.com/watch?v=a4Z0iac_6Lk"
source = pafy.new(url).getbest()
capture = cv2.VideoCapture(source.url)
color = "red"
red = 0
green = 0



#-- Demo: segnale sonoro
duration = 1000  # millisecondi
freq = 440  # Hz
#--



while (True):
    # Catturo ogni frame del video
    ret, current_frame = capture.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):   # Quitta se si preme il tasto "q" (spiegazione: https://stackoverflow.com/a/57691103)
        break

    current_frame_cropped = current_frame[50:500, 475:505,:] # (spiegazione: https://stackoverflow.com/a/58177717/15553356)

    # Converto in HSV
    hsv = cv2.cvtColor(current_frame_cropped, cv2.COLOR_BGR2HSV)

    # Definisco il range dei colori in HSV da cercare
    lower_val_buy = np.array([40, 40,40])
    upper_val_buy = np.array([70,255,255])

    lower_val_sell = np.array([0,0,255])
    upper_val_sell = np.array([5,255,255])

    # Creo una maschera, selezionando solamente i colori sopra definiti
    mask_buy = cv2.inRange(hsv, lower_val_buy, upper_val_buy)
    mask_sell = cv2.inRange(hsv, lower_val_sell, upper_val_sell)

    # Applico una maschera
    res_buy = cv2.bitwise_and(current_frame_cropped,current_frame_cropped,mask=mask_buy)
    res_sell = cv2.bitwise_and(current_frame_cropped,current_frame_cropped,mask=mask_sell)

    # Faccio qualche operazione (erosione, dilatazione) per evidenziare meglio l'area rossa "Sell"
    kernel = np.ones((2,2), np.uint8)
    res_sell = cv2.erode(res_sell, kernel, iterations=1)
    res_sell = cv2.dilate(res_sell, kernel, iterations=3)
    res_buy = cv2.erode(res_buy, kernel, iterations=2)
    res_sell = cv2.dilate(res_sell, kernel, iterations=3)

    # Metto gli elemento in un solo pannello
    fin = np.hstack((current_frame_cropped,res_buy,res_sell))

    # Mostro il pannello
    cv2.imshow("frame", fin)

    # Se applicando la maschera restano degli elementi (=> esistono delle aree verdi), sum sarà > 0
    hasGreen = np.sum(mask_buy)
    hasRed = np.sum(mask_sell)
    if hasGreen > 0 and hasRed > 0:
        continue
    else:
        if hasGreen > 0 and green == 0 and color == "green":
            print("Buy")
            color = "red"
            green = 1
            red = 0
            winsound.Beep(freq, duration)
        if hasRed > 0 and red == 0 and color == "red":
            print("Sell")
            color = "green"
            green = 0
            red = 1
            winsound.Beep(freq, duration)
