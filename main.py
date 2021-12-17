import cv2
import pafy
import time
import numpy as np
import winsound # Demo: segnale sonoro
from PIL import Image
# from matplotlib import cm

url = "https://www.youtube.com/watch?v=yYSkSzsxDSI"
source = pafy.new(url).getbest()
capture = cv2.VideoCapture(source.url)
color = "red"
red = 0
green = 0

p = 120



#-- Demo: segnale sonoro
duration = 1000  # millisecondi
freq = 440  # Hz
#--



while (True):
    # Catturo ogni frame del video
    ret, current_frame = capture.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):   # Quitta se si preme il tasto "q" (spiegazione: https://stackoverflow.com/a/57691103)
        break

    # current_frame = current_frame[50:400, 75:505,:]

    img = Image.fromarray(current_frame, 'RGB')

    #time.sleep(2)

    imgSmall = img.resize((p,p),resample=Image.BILINEAR)
    result = imgSmall.resize(img.size,Image.NEAREST)

    result_array = np.array(result)

    result_array = result_array[50:500, 480:500,:]

    #current_frame_cropped = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    current_frame_cropped_sell = cv2.cvtColor(result_array, cv2.COLOR_RGB2BGR)

    #hsv = cv2.cvtColor(current_frame_cropped, cv2.COLOR_BGR2HSV)
    hsvSell = cv2.cvtColor(current_frame_cropped_sell, cv2.COLOR_RGB2HSV)

    lower_val_buy = np.array([40, 40,40])
    upper_val_buy = np.array([70,255,255])

    lower_val_sell = np.array([0,0,220])
    upper_val_sell = np.array([60,360,260])

    mask_buy = cv2.inRange(hsvSell, lower_val_buy, upper_val_buy)
    mask_sell = cv2.inRange(hsvSell, lower_val_sell, upper_val_sell)

    res_buy = cv2.bitwise_and(current_frame_cropped_sell,current_frame_cropped_sell,mask=mask_buy)
    res_sell = cv2.bitwise_and(current_frame_cropped_sell,current_frame_cropped_sell,mask=mask_sell)

    fin = np.hstack((current_frame_cropped_sell,res_sell,res_buy))

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
