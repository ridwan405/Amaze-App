
from pathlib import Path
import os
from deepface import DeepFace

# source: https://github.com/serengil/deepface

BASE_DIR = Path(__file__).resolve().parent.parent

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

metrics = ["cosine", "euclidean", "euclidean_l2"]


#RetinaFace and MTCNN seem to overperform in detection and alignment stages but they are much slower.
# If the speed of your pipeline is more important, then you should use opencv or ssd. On the other hand,
# if you consider the accuracy, then you should use retinaface or mtcnn.
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]


#args are names for img, stream = True if we are looping (real time verifaction) with time.sleep(seconds)
# or need  faster verification speed
#returns boolean
#img1 will  be name of webcam img
#img 2 will be name of img and will come from database
def imgVerify(img1, img2, stream):
    
    # will be path for webcam images
    path1= BASE_DIR/'amazapp'
    img1_path= os.path.join(path1, img1)
    
     # will be path for user images in db
    path2= BASE_DIR/'amazapp'/'core'/'utils'/'db'
    img2_path= os.path.join(path2, img2)
    
    if stream:
        detector_backend = backends[1] #ssd
    else:
        detector_backend = backends[3] #mtcnn
    
    
    match= DeepFace.verify(img1_path = img1_path, img2_path = img2_path, model_name = models[2],
                           distance_metric = metrics[2], detector_backend = detector_backend)
    
    if match['verified'] :
        print("Face matched")
    else:
        print("Face did not match")
    
    return match['verified']



# print(imgVerify('mark.jpg','chris1.jpg', True))

#python face_recognition.py





