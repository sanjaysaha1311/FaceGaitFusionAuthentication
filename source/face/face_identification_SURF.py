"""
Created by Sanjay at 4/10/2020

Feature: Enter feature name here
Enter feature description here
"""

import cv2
from sklearn.ensemble import RandomForestClassifier

from source.utils.common_functions import report_results
import numpy as np
from source.face.FisherFace import read_faces
from source.utils.utils import *

K_LIST = [x for x in range(3, 16, 2)]  # for k-nearest neighbors
N_ESTIMATORS = [25, 50, 100, 200]  # for random forest


def extract_surf(img):
    """
    Extract SURF keypoints and descriptors from an image
    """
    # surf = cv2.SURF(hessianThreshold=hessian, nOctaves=octave, nOctaveLayers=octaveLayers, extended=ext)
    surf = cv2.xfeatures2d.SURF_create()
    kp, des = surf.detectAndCompute(img, None)

    return kp, des


if __name__ == '__main__':
    train_faces, train_labels = read_faces(FACE_TRAIN_DIR, dont_squeeze=True)  # read faces, labels (train)
    test_faces, test_labels = read_faces(FACE_TEST_DIR, dont_squeeze=True)  # read faces, labels (test)

    train_x, train_y = [], []
    for img, lbl in zip(train_faces, train_labels):
        key_points, descriptors = extract_surf(img)
        for d in descriptors:
            train_x.append(d)
            train_y.append(lbl)

    # print('# ======================= SVC ========================= #')
    # c = list(zip(train_x, train_y))
    # random.shuffle(c)
    # train_x, train_y = zip(*c)
    # svc = SVC(kernel='linear', C=10000, gamma=0.1)
    # svc.fit(train_x, train_y)
    #
    # test_y, pred_y = [], []
    # for img, lbl in zip(test_faces, test_labels):
    #     key_points, descriptors = extract_surf(img)
    #     pred_list = svc.predict(descriptors)
    #     counts = np.bincount(pred_list)  # bin counting for upcoming argmax
    #     pred = np.argmax(counts)
    #     pred_y.append(pred)
    #     test_y.append(lbl)
    #
    # score, confusion_matrix, report = report_results_face(test_y, np.array(pred_y), cmat_flag=True)

    # print('# ======================= K-Nearest Neighbors ========================= #')
    # acc_list = []
    # for k in K_LIST:
    #     knn = KNeighborsClassifier(n_neighbors=k)
    #     knn.fit(train_x, train_y)
    #     test_y, pred_y = [], []
    #     for img, lbl in zip(test_faces, test_labels):
    #         key_points, descriptors = extract_surf(img)
    #         pred_list = knn.predict(descriptors)
    #         counts = np.bincount(pred_list)  # bin counting for upcoming argmax
    #         pred = np.argmax(counts)
    #         pred_y.append(pred)
    #         test_y.append(lbl)
    #     # knn_pred_y = knn.predict(test_x)
    #     print('k-neighbors: %d' % k)
    #     score, confusion_matrix, report = report_results_face(test_y, pred_y)
    #     acc_list.append(score)
    # print()

    print('# ======================= Random Forest ========================= #')
    acc_list_rf = []
    for n in N_ESTIMATORS:
        rand_forest = RandomForestClassifier(n_estimators=n)
        rand_forest.fit(train_x, train_y)
        test_y, pred_y = [], []
        for img, lbl in zip(test_faces, test_labels):
            key_points, descriptors = extract_surf(img)
            pred_list = rand_forest.predict(descriptors)
            counts = np.bincount(pred_list)  # bin counting for upcoming argmax
            pred = np.argmax(counts)
            pred_y.append(pred)
            test_y.append(lbl)
        score, confusion_matrix, report = report_results(test_y, pred_y)
        acc_list_rf.append(score)
        print('Tree count: %d \t Accuracy: %.3f' % (n, score))
    print()