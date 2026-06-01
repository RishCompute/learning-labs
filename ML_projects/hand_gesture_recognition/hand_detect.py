import cv2
import numpy as np
import pandas as pd
import csv
import joblib

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def remove_face_from_mask(frame, mask):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80),
    )


    for (x, y, w, h) in faces:

        pad_x = int(w * 0.10)
        pad_y = int(h * 0.20)
        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(mask.shape[1], x + w + pad_x)
        y2 = min(mask.shape[0], y + h + pad_y)
        mask[y1:y2, x1:x2] = 0
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return mask

def draw_hull_points(frame, contours):
    for cnt in contours:
        hull_indices = cv2.convexHull(cnt , returnPoints=False)
        hull = cv2.convexHull(cnt)
        cv2.drawContours(frame, [hull], -1, (0, 255, 255), 2)
        return  hull_indices, hull


def draw_convexity_defects(frame , contours ):
    for cnt in contours:
        hull_indices = cv2.convexHull(points =cnt ,returnPoints=False)
        defects = cv2.convexityDefects(cnt , hull_indices)
        for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                if d > 10000 :
                    start = tuple(cnt[s][0])
                    end   = tuple(cnt[e][0])
                    far   = tuple(cnt[f][0])
                    cv2.line(frame, start, end, (255, 0, 0), 2)
                    cv2.circle(frame, far, 6, (0, 0, 255), -1)


def create_contours( mask ,  min_area=15000, max_hands=1):
    contours, _ = cv2.findContours(
        mask.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    if not contours:
        return 0 , 0

    hand_contours = [
        contour
        for contour in contours
        if cv2.contourArea(contour) >= min_area
    ]

    if not hand_contours:
        return  0, 0

    hand_contours = sorted(hand_contours, key=cv2.contourArea, reverse=True)[:max_hands]
    hand_count = len(hand_contours)

    # if hand_contours != None:
    #     dataset_creation(hand_contours , fing_index = 4)
    if hand_contours is not None:
        return (hand_contours , hand_count)


                
def draw_hand_contours(frame , hand_contours):
    
    for index, contour in enumerate(hand_contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


def rel_cont_area(hand_contours):
    cont_area = np.array([cv2.contourArea(cnt) for cnt in hand_contours ])
    rect_list = [cv2.boundingRect(cnt) for cnt in hand_contours]
    rect_area = np.array([w * h for x ,y ,w ,h in rect_list])
    rel_area =  cont_area / rect_area
    return rel_area


def rel_hull_area(hand_contours):
    hull_list = [cv2.convexHull(points =cnt ) for cnt in hand_contours]
    hull_area = np.array([cv2.contourArea(cnt) for cnt in hull_list ])
    rect_list = [cv2.boundingRect(cnt) for cnt in hand_contours]
    rect_area = np.array([w * h for x ,y ,w ,h in rect_list])
    rel_area =  hull_area/ rect_area
    return rel_area


def num_defects(hand_contours):
    hull_indices = [cv2.convexHull(points =cnt ,returnPoints=False) for cnt in hand_contours]
    n_defects = np.array([len(cv2.convexityDefects(cnt , index )) for cnt , index in zip(hand_contours , hull_indices) ])
    return n_defects.astype(np.float64)


def sum_angles(hand_contours):
    angles = []
    for cnt in hand_contours:
        hull_indices =cv2.convexHull(points =cnt ,returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull_indices ) 
        for i in range(defects.shape[0]):
            s ,e ,f ,d = defects[i ,0]
            start = cnt[s][0]
            end   = cnt[e][0]
            far   = cnt[f][0]
            x1 = start - far
            x2 = end - far
            cosine = np.dot(x1 ,x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))
            angle = abs(np.arccos(cosine))
            angles.append(angle)
    return np.array([np.sum(angles)])


def dataset_creation( hand_contour ,  fing_index ):
    rel_h_area = rel_hull_area(hand_contour)
    rel_c_area = rel_cont_area(hand_contour)
    n_defects = num_defects(hand_contour)
    angles = sum_angles(hand_contour)
    df = pd.DataFrame(columns = ['rel_cont_area' , 'rel_hull_area' , 'num_defects','sum_angles', 
                                'thumb' , 'index' ,'middle' , 'ring' , 'pinky'])
    
    df.loc[0,'rel_cont_area'] = rel_c_area
    df.loc[0,'rel_hull_area'] = rel_h_area
    df.loc[0,'num_defects'] = n_defects
    df.loc[0,'sum_angles'] = angles

    match fing_index:
        case 0 :
            df.loc[0,['index' ,'middle' , 'ring' , 'pinky']] = 0
            df.loc[0,['thumb']] = 1
        case 1 :
            df.loc[0,['thumb' ,'middle' , 'ring' , 'pinky']] = 0
            df.loc[0,['index']] = 1
        case 2 :
            df.loc[0,['thumb' , 'ring' , 'pinky']] = 0
            df.loc[0,['index','middle']] = 1
        case 3 :
            df.loc[0,['thumb' , 'pinky']] = 0
            df.loc[0,['index' ,'middle','ring']] = 1
        case 4 :
            df.loc[0,['thumb']] = 0
            df.loc[0,['index' ,'middle' , 'ring' ,'pinky']] = 1
        case 5 :
            df.loc[0,['index' ,'middle' , 'ring' , 'thumb','pinky']] = 1
            
    new_row = df.iloc[0]

    with open("data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)    


def features(hand_contour):
    rel_h_area = rel_hull_area(hand_contour)[0]
    rel_c_area = rel_cont_area(hand_contour)[0]
    n_defects  = num_defects(hand_contour)[0]
    angles     = sum_angles(hand_contour)[0]
    scaler = joblib.load('hand_gesture_scaler.pkl')
    
    if len([rel_c_area]) == 1:
        return scaler.transform(np.array([rel_c_area , rel_h_area , n_defects , angles]).reshape((1,-1)))


def predict_pipeline(x):
    model = joblib.load('knn_clf_hand_gesture.pkl')
    return model.predict(x)


def fing_count(x):
    return np.sum(x)
     

while True:

    
    ret , frame = cap.read()
    if not ret:
        break


    frame = cv2.flip(frame , 1)


    blur = cv2.GaussianBlur(frame, (7,7), 0)


    img_YCrCb = cv2.cvtColor(blur, cv2.COLOR_BGR2YCR_CB)
    YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135 , 85), (255,180,135)) 
    YCrCb_mask = remove_face_from_mask(frame, YCrCb_mask)
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((7,7), np.uint8))
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8))


    (hand_contours , hand_count)= create_contours( YCrCb_mask)


    if hand_count == 1 :
        draw_hand_contours(frame , hand_contours)
        draw_hull_points(frame, hand_contours)
        draw_convexity_defects(frame , hand_contours)

        x = features(hand_contours)
        predicted = predict_pipeline(x.reshape((1,-1)))
        print( 'Number of fingers', fing_count(predicted))
    

    if hand_count == 0:
        print("No hand detected") 


    cv2.imshow("mask", YCrCb_mask)
    cv2.imshow("img" , frame)


    if cv2.waitKey(1) == 27 :
        break
  

cap.release()
cv2.destroyAllWindows()

