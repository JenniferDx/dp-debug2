from PyQt5 import QtCore, QtGui, uic, QtWidgets
import cv2
import draw_bboxes
import gt_read
import sys,os


class ImgView(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ImgView, self).__init__(parent)
        uic.loadUi('qt/show_img.ui', self)
        self.maxW = 500
        self.maxH = 400
        self.ImageView.setGeometry(20, 20, self.maxW, self.maxH)
        #self.ImageView.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.resize(self.ImageView.width()+40, self.ImageView.height()+40)


    def showImage(self, image_path):
        img = QtGui.QImage(image_path)
        vieww = self.maxW
        viewh = self.maxH
        imgw = img.width()
        imgh = img.height()

        #if image out of view range, scale img
        if imgw > self.maxW or imgh > self.maxH:
            if imgw * viewh * 1.0 / vieww > imgh:
                img = img.scaled(vieww, int(vieww * imgh * 1.0 / imgw))
            else:
                img = img.scaled(int(viewh * imgw * 1.0/imgh), viewh)
        else:
            self.ImageView.setGeometry(20, 20, imgw, imgh)
            self.resize(self.ImageView.width() + 40, self.ImageView.height() + 40)

        self.ImageView.setPixmap(QtGui.QPixmap.fromImage(img))


    def show_img_with_gt(self, img_p, gt_path):
        #print(img_p,gt_path)
        image = cv2.imread(img_p)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        oriented_bboxes, bboxes, gxs, gys, ignored = gt_read.read_gt(gt_path, gt_format='icdar2015',
                                                                     gt_type='oriented_bboxes')
        #print(oriented_bboxes)
        draw_bboxes.draw_oriented_bboxes_with_ignore(image, oriented_bboxes, ignored)

        tmpp = "./tmp/tmp.jpg"
        cv2.imwrite(tmpp, image)
        img = QtGui.QImage(tmpp)
        #os.remove(tmpp)
        self.showImage(tmpp)



