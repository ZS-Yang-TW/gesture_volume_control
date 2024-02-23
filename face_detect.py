import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)  # 載入人臉模型
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    faces = face_cascade.detectMultiScale(img)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (127, 76, 45), 4)

    cv2.imshow("img", img)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
