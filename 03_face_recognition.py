#################### MEVCUT RESİMLERE GÖRE GERÇEK ZAMANLI TANIMA İŞLEMİ GERÇEKLEŞTİRİR ######################################

import cv2
import numpy as np
import os 
# %%

def faceNames(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
#    print(imagePaths)
    name=[]
    for imagePath in imagePaths:
        name.append(os.path.split(imagePath)[-1].split(".")[2])
#        print(os.path.split(imagePath)[-1])
    return name

# %%
def main():
#    radius=1,neighbors=1,grid_x=8,grid_y=8,threshold=60
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1,neighbors=1,grid_x=8,grid_y=8,threshold=60)
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    path="dataset\\"
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    names=[]
    name=faceNames(path)
    [names.append(x) for x in name if x not in names]
    while True:
    
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically
    
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
    
        for(x,y,w,h) in faces:
    
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print(id,confidence)
            
            
            # Check if confidence is less them 100 ==> "0" is perfect match 
            #confidence=100-confidence
            if (confidence < 68):
                id = names[id]
            #confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "Tanimsiz"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
    
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    
    # Do a bit of cleanup
    print("\n [BILGI] Programdan Çıkılıyor")
    cam.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()