#coding:utf-8
# 打开摄像头并灰度化显示
from face_class import Face_Recognition as Fc
import cv2
from imutils import face_utils



capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
people=[]

fc = Fc()
p1 = fc.LoadFaceData('LinYongHao')
people.append(p1)

RIGHT_EYE_START = 37-1
RIGHT_EYE_END = 42 -1
LEFT_EYE_START = 43-1
LEFT_EYE_END = 48-1
EAR_AR_THRESH = 0.3
EAR_AR_CONSEC_FRAMES = 4


num = 0 #眨眼
Face_Result = False
while(True):
    # 获取一帧
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    start = cv2.getTickCount()
    face = fc.GetFaceData(frame)
    end = cv2.getTickCount()
    if len(face)== 1 :
        vector = fc.create128DvectorSpace(frame,face[0])
        if Face_Result == False:
            for i in range(len(people)):

                Face_Result = fc.CompareFace(vector, people[i])
                print('人脸检测成功，请眨眼')
                if Face_Result:
                    people_num = i
                    break



        else:
            print('请眨眼')
            shape = fc.Face_Predictor(frame, face[0])
            points = face_utils.shape_to_np(shape)
            leftEye = points[LEFT_EYE_START:LEFT_EYE_END + 1]
            rightEye = points[RIGHT_EYE_START:RIGHT_EYE_END + 1]
            leftEAR = fc.ComputeEAR(leftEye)
            rightEAR = fc.ComputeEAR(leftEye)
            EAR = (leftEAR + rightEAR) / 2.0  # 求左右眼EAR的均值
            if EAR < EAR_AR_THRESH:
                num += 1
            elif num >= EAR_AR_CONSEC_FRAMES:
                print("-"*10+fc.GetPersonName(people_num)+',请进'+"-"*10)
                num = 0
                Face_Result = False

    else:
        print('人脸检测失败，请重新刷脸')






    print((end-start)/cv2.getTickFrequency())
    cv2.imshow('Goodhao', frame)
    if cv2.waitKey(1) == ord('q'):
        break