import cv2  #opencv 影像處理的套件
import numpy as np #矩陣運算
import time #用來取得電腦時間
import mediapipe as mp #偵測模型
import math #偵測模型


#實現音量控制所需的套件:
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    #音量控制套件
# import osascript #音量控制套件 (For macOS)


##攝影機設定##
cam_width , cam_height = 640, 480
cap = cv2.VideoCapture(0) #填入0或1試試看
cap.set(3, cam_width)   #調整影像寬度
cap.set(4, cam_height)   #調整影像長度

##手部模型偵測參數設定、功能引入##
mphands = mp.solutions.hands  #使用medidapipe裡的手部辨識功能
hands = mphands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5) #設定手部辨識模型
mpDraw = mp.solutions.drawing_utils #繪畫工具

##手部骨架樣式設定##
handLms_style = mpDraw.DrawingSpec(color=(73,93,70), thickness=6)  #手座標樣式
handCon_style = mpDraw.DrawingSpec(color=(255,250,240), thickness=3) #手連接樣式

##FPS計算參數設定##
current_time = 0
previous_time = 0

##音量控制相關設定##
vol = 0 #初始化音量大小
volbar = 400 #初始化音量指示條頂的位置
volper = 0  #初始化音量百分比數值

##取得裝置的音量範圍##
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()  #取得裝置音量範圍資料
minVol, maxVol = volRange[0], volRange[1]   #取得裝置音量最大值、最小值
print(volume.GetVolumeRange())  #輸出音量範圍   (-96,0,後面這個不用理他)

# # macOS 系统音量控制函数
# def set_volume(volume):
#     osascript.run(f"set volume output volume {volume}")

##迴圈區域##
while True:
    ret, img = cap.read()
    #hand_detection
    if ret:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      #bgr轉rgb
        result = hands.process(img_rgb)

        img_height = img.shape[0]
        img_width = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:     #畫出每個手的座標及連線、設定樣式
                mpDraw.draw_landmarks(img, handLms,mphands.HAND_CONNECTIONS, handLms_style, handCon_style)
                    
                for i, lm in enumerate(handLms.landmark):       #輸出每個手的座標點 
                    xPos = int(lm.x * img_width)    #比例乘上寬度
                    yPos = int(lm.y * img_height)   #比例乘上高度
                    
                    #記錄拇指與食指座標
                    if (i == 4):
                        x4, y4 = xPos, yPos
                    if (i == 8):
                        x8, y8 = xPos, yPos
                
                xm , ym = (x4+x8)//2 , (y4+y8)//2   #取得中點座標
                
                #計算拇指、食指兩點的長度，並設定觸發事件
                length = math.hypot(x8-x4, y8-y4)   #用square root計算長度
                
            #映射調整
            vol = np.interp(length,[25,200],[-30,maxVol])   #音量映射調整
            volbar = np.interp(length,[25,200],[400,150])   #指示條長度映射調整
            volper = np.interp(length,[25,200],[0,100])   #指示條數值映射調整
            volume.SetMasterVolumeLevel(vol, None)  #設定音量    
            
            # # 映射調整（适用于 macOS）
            # vol = np.interp(length, [25, 200], [0, 100])  # 音量映射調整为百分比
            # volbar = np.interp(length, [25, 200], [400, 150])  # 指示條長度映射調整
            # volper = np.interp(length, [25, 200], [0, 100])  # 指示條數值映射調整
            # set_volume(vol)  # 设置系统音量
                
            #畫出拇指、食指、中指三個點，並連線
            cv2.circle(img, (x4, y4), 9, (105,165,218), cv2.FILLED)
            cv2.circle(img, (x8, y8), 9, (105,165,218), cv2.FILLED)
            cv2.circle(img, (xm, ym), 9, (105,165,218), cv2.FILLED)
            cv2.line(img,(x4, y4),(x8, y8),(105,165,218),3)
            
            if (length <= 25)|(length >= 200):        #手指捏起來的時候，中點變色 (設定觸發事件)
                cv2.circle(img, (xm, ym), 9, (34,34,78), cv2.FILLED)
    
    #計算幀率
    current_time = time.time()  #取得當下的時間
    fps = 1/(current_time-previous_time)    #算出"週期"，倒數後變成"頻率"
    previous_time = current_time    #記錄當下的時間，當作下次算週期的參考。
    
    #畫出指示框、指示條、顯示幀率、音量百分比
    cv2.rectangle(img,(50,150),(85,400),(105,165,218),3)  #指示條外框
    cv2.rectangle(img,(50,int(volbar)),(85,400),(105,165,218),cv2.FILLED)   #指示條填滿
    cv2.putText(img,f"FPS:{int(fps)}",(30,50), cv2.FONT_HERSHEY_DUPLEX, 1.5, (49,68,52), 3)  #fps標籤
    cv2.putText(img,f"{int(volper)}%",(40,450), cv2.FONT_HERSHEY_DUPLEX, 1,(105,165,218), 2)  #音量數值標籤    
                
    cv2.imshow("img",img)

    if cv2.waitKey(1) == ord('q'):
        break