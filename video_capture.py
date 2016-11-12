import cv2

cap = cv2.VideoCapture(0)

print cap.isOpened()

cv2.namedWindow("edges",1);

while True:
    frame = cap.read()
    if frame[0]:
        edges = cv2.cvtColor(frame[1], cv2.COLOR_BGR2GRAY);
        edges = cv2.GaussianBlur(edges, (7, 7), 1.5, 1.5);
        edges = cv2.Canny(edges, 0, 30, 3);
        cv2.imshow("edges", edges);
    if cv2.waitKey(30) >= 0:
        break

cv2.waitKey(0)
