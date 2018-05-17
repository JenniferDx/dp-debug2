from PyQt5 import QtCore, QtGui, uic, QtWidgets
import img_view
class ImgViewContrl(QtWidgets.QWidget):
    view_closed = QtCore.pyqtSignal()
    def __init__(self, parent = None):
        super(ImgViewContrl, self).__init__(parent)
        uic.loadUi('qt/img_view_control.ui', self)
        self.setWindowTitle('Image View Contorl Panel ')
        self.QcheckImgGt.setCheckState(QtCore.Qt.Checked)
        self.QcheckOriImg.setCheckState(QtCore.Qt.Unchecked)
        self.QcheckPredImg.setCheckState(QtCore.Qt.Checked)
        self.img_view_list={
            'ori_img': 0,
            'img_with_gt':1,
            'img_with_pred_box':0
        }
        self.refresh_check_state()
        self.img_views={}
        self.init_view()

        self.img_path=''
        self.gt_path=''
        self.pred_path=''

        #slots and signals
        self.QcheckImgGt.stateChanged.connect(self.refresh_check_state)
        self.QcheckOriImg.stateChanged.connect(self.refresh_check_state)
        self.QcheckPredImg.stateChanged.connect(self.refresh_check_state)

    def syncSelectItems(self, img_path, gt_path, pred_path):
        self.img_path = img_path
        self.gt_path = gt_path
        self.pred_path = pred_path

    def refresh_check_state(self):
        if self.QcheckOriImg.checkState() == QtCore.Qt.Checked:
            self.img_view_list['ori_img'] = 1
        else:
            self.img_view_list['ori_img'] = 0
        if self.QcheckImgGt.checkState() == QtCore.Qt.Checked:
            self.img_view_list['img_with_gt'] = 1
        else:
            self.img_view_list['img_with_gt'] = 0
        if self.QcheckPredImg.checkState() == QtCore.Qt.Checked:
            self.img_view_list['img_with_pred_box'] = 1
        else:
            self.img_view_list['img_with_pred_box'] = 0

    def init_view(self):
        for view_name in self.img_view_list.keys():
            self.img_views[view_name] = img_view.ImgView()
            self.img_views[view_name].setWindowTitle(view_name)

    def refresh(self, img_path, gt_path, pred_path):
        if self.img_view_list['ori_img']:
            self.img_views['ori_img'].showImage(img_path)
            self.img_views['ori_img'].show()
        if self.img_view_list['img_with_gt']:
            self.img_views['img_with_gt'].show_img_with_gt(img_path, gt_path)
            self.img_views['img_with_gt'].show()
        if self.img_view_list['img_with_pred_box']:
            self.img_views['img_with_pred_box'].show_img_with_gt(img_path, pred_path)
            self.img_views['img_with_pred_box'].show()

    #def calPerformance(self):
        # from script_test_ch4 import get_performance
        # get_performance.get_performance(pred_txt_path)


    def closeEvent(self, event):
        for view_name in self.img_view_list.keys():
            if self.img_view_list[view_name]:
                self.img_views[view_name].close()
                self.img_view_list[view_name] = 0
                self.img_views[view_name] = None
            else:
                self.img_views[view_name] = None
        self.view_closed.emit()
        self.close()





