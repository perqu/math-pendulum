import cv2, csv
       

def find_largest_cluster(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = max(contours, key=cv2.contourArea)

    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    else:
        return None

### Check if video is valid ###
cap = cv2.VideoCapture('vds/video4.mp4')
ret, frame = cap.read()
if not ret:
    print("Error reading the first frame of the video")
    exit()

movement = []
knn = cv2.createBackgroundSubtractorKNN(dist2Threshold=800)
while True:
    mask = knn.apply(frame)
    center_of_mass = find_largest_cluster(mask)
    movement.append((center_of_mass[0], center_of_mass[1], round(cap.get(cv2.CAP_PROP_POS_MSEC)/1000,3)))

    '''
    if center_of_mass is not None:
        cv2.drawMarker(frame, center_of_mass, color=(255, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=5)
    cv2.imshow('Video', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    '''

    ret, frame = cap.read()
    if not ret:
        break

with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(movement)

cap.release()
cv2.destroyAllWindows()
