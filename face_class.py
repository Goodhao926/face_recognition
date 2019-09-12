# -*- coding: utf-8 -*-
import dlib
import cv2
import numpy as np
from scipy.spatial import distance


class Face_Recognition:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()  # 获取人脸分类器
        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        face_recogniton_path = 'dlib_face_recognition_resnet_model_v1.dat'
        self.predictor = dlib.shape_predictor(predictor_path)
        self.face_recogniton = dlib.face_recognition_model_v1(face_recogniton_path)
        self.name=[]
    def GetFaceData(self, img):  # 人脸矩形区域数组
        detectors = self.detector(img, 2)
        return detectors

    def create128DvectorSpace(self, img, face):  # img 为图片，face 为 人头矩形区域
        # dets = self.detector(img, 1)
        # for index, face in enumerate(dets):  # 遍历多个人脸
        shape = self.predictor(img, face)
        return self.face_recogniton.compute_face_descriptor(img, shape)

    def CompareFace(self, data1, data2):  # 128维数组

        diff = 0
        for i in range(len(data1)):
            # print(data1[i])
            diff += (data1[i] - data2[i]) ** 2
        diff = np.sqrt(diff)
        if (diff < 0.5):
            return True
        else:
            return False

    def SaveFaceData(self, data, name):  # 128向量值
        vector = np.array([])
        # path = "/" + name + '.npy'
        for index, num in enumerate(data):
            vector = np.append(vector, num)
        np.save(name, vector)
        return vector

    def LoadFaceData(self, name):  # 返回128向量数据
        if name != None:
            data = np.load( name + '.npy')
            self.name.append(name)
        return data

    def Face_Predictor(self, img, rect):  # ,矩形区域 返回特征点
        return self.predictor(img, rect)

    def ComputeEAR(self,eye):
            # print(eye)
            A = distance.euclidean(eye[1], eye[5])
            B = distance.euclidean(eye[2], eye[4])
            C = distance.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear

    def GetPersonName(self,i):
        return self.name[i]

img = cv2.imread('LinJieHuan.jpg')
fc = Face_Recognition()
shape = fc.GetFaceData(img)
r = fc.create128DvectorSpace(img,shape[0])
fc.SaveFaceData(r,'LinJieHuan')


