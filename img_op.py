import draw_bboxes
import gt_read
import cv2
import sys,os
import numpy as np
from PyQt5 import QtGui
def numpy_2_Qpixmap(data):
    #data:[h, w, 3]
    data = np.array(data,dtype=np.uint32)
    width = data.shape[1]
    height = data.shape[0]
    img = QtGui.QImage(width, height, QtGui.QImage.Format_RGB32)
    for x in xrange(width):
        for y in xrange(height):
            img.setPixel(x, y, QtGui.QColor(*data[y][x]).rgb())
    pix = QtGui.QPixmap.fromImage(img)
    return pix
def show_img_with_gt(img_p, gt_path):
    image = cv2.imread(img_p)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    oriented_bboxes, bboxes, gxs, gys, ignored = gt_read.read_gt(gt_path, gt_format='icdar2015', gt_type='oriented_bboxes')
    draw_bboxes.draw_oriented_bboxes_with_ignore(image, oriented_bboxes, ignored)
    tmpp="./tmp/tmp.jpg"
    cv2.imwrite(tmpp,image)
    img = QtGui.QImage(tmpp)
    os.remove(tmpp)
    return img