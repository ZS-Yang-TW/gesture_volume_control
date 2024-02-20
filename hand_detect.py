import cv2
import mediapipe as mp
import time    #算fps要用的

cap = cv2.VideoCapture(0) #填入0或1試試看

##手部模型偵測參數設定、功能引入##
mphands = mp.solutions.hands  #使用medidapipe裡的hands函式庫
hands = mphands.Hands(max_num_hands=6,min_detection_confidence=0.01,min_tracking_confidence=0.5) #呼叫hands函式
mpDraw = mp.solutions.drawing_utils #呼叫畫點函式

##手部骨架樣式設定##
handLms_style = mpDraw.DrawingSpec(color=(127,255,0), thickness=6)  #手座標樣式
handCon_style = mpDraw.DrawingSpec(color=(255,250,240), thickness=3) #手連接樣式

##FPS計算參數設定##
current_time = 0    #目前時間初始化
previous_time = 0   #先前時間初始化

##迴圈區域##
while True:
    ret, img = cap.read()       #讀取鏡頭
    background = cv2.imread('background.jpg')
    
    if ret:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      #bgr轉rgb
        result = hands.process(img_rgb)
        #print(result.multi_hand_landmarks)

        img_height = img.shape[0]
        img_width = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:     #畫出每個手的座標及連線、設定樣式
                mpDraw.draw_landmarks(img, handLms,mphands.HAND_CONNECTIONS, handLms_style, handCon_style)
                mpDraw.draw_landmarks(background, handLms,mphands.HAND_CONNECTIONS, handLms_style, handCon_style)
                
                for i, lm in enumerate(handLms.landmark):       #輸出每個手的座標點 
                    xPos = int(lm.x * img_width)    #比例乘上寬度
                    yPos = int(lm.y * img_height)   #比例乘上高度
                    cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,69,255), 1)   #加上標籤
                    cv2.putText(background, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,69,255), 1)   #加上標籤

                    if (i ==4)|(i ==8)|(i ==12)|(i ==16)|(i ==20):  
                        cv2.circle(img, (xPos, yPos), 9, (34,139,34), cv2.FILLED)
                    
                    print(i, xPos, yPos)
        
        #計算fps
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        previous_time = current_time

        #加入fps標籤
        cv2.putText(img, f"FPS: {int(fps)}", (30,50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (105,165,218), 2)

        
        cv2.imshow('img', img)
        cv2.imshow('background', background)

    if cv2.waitKey(1) == ord('q'):
        break
