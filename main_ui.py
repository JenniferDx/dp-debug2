import sys, os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import img_op
import Img_view_control
from PyQt5 import *
qtCreatorFile = "./qt/dp-debug.ui" #.ui Window File
default_path = '/media/duxiaowei/disk2t/dataset/ICDAR2015/task1/ch4_test_images'
default_gt_path = '/media/duxiaowei/disk2t/dataset/ICDAR2015/task1/ch4_test_localization_transcription_gt'
default_pred_path = '/home/duxiaowei/disk2t/models/seglink_bgs'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #some setting
        self.setWindowTitle("Main Control Panel")


        #other self variables

        files = os.listdir(default_path)
        filename = files[0]
        self.gt_path = default_gt_path
        self.img_path = default_path
        self.filename =filename
        self.gt_name = get_gt_name(filename)
        self.pred_path = default_pred_path
        self.pred_name = get_res_name(self.filename)
        #init default value

        self.filelists.addItems(files)
        self.filelists.setCurrentRow(0)
        self.refreshIndicatorObjects()

        #signal and slots
        self.open.clicked.connect(self.choosePath)
        self.open_file.clicked.connect(self.chooseFiles)
        self.filelists.itemSelectionChanged.connect(self.selectedFileChanged)
        self.edit_path.textChanged.connect(self.refreshViews)
        self.change_gt_path.clicked.connect(self.changeGtPath)
        self.QBImagView.clicked.connect(self.open_image_view)
        self.QBChangeLogPath.clicked.connect(self.changeLogPath)
        self.QCal.clicked.connect(self.calPerformance)


        #different views
        self.viewlists={
            'img_view': 0
        }

    def changeGtPath(self):
        self.gt_path = getDirectory()
        self.edit_gt_path.setText(os.path.join(self.gt_path, get_gt_name(self.filename)))


    def chooseFiles(self):
        self.filelists.clear()
        choosed_files = getFiles()
        filenames = [filename.split('/')[-1] for filename in choosed_files]
        self.filelists.addItems(filenames)
        self.filelists.setCurrentRow(0)
        self.filename = filenames[0]
        self.gt_name = get_gt_name(self.filename)
        self.pred_name = get_res_name(self.filename)
        self.img_path = os.path.dirname(self.choosed_files[0])
        self.refreshIndicatorObjects()

    def choosePath(self):
        self.filelists.clear()
        choosed_path = getDirectory()
        files = os.listdir(choosed_path)
        self.filelists.addItems(files)
        self.filelists.setCurrentRow(0)
        self.img_path = choosed_path
        self.filename = files[0]
        self.pred_name = get_res_name(self.filename)
        self.gt_name = get_gt_name(self.filename)
        self.refreshIndicatorObjects()

    def changeLogPath(self):
        self.pred_path = getDirectory()
        self.pred_name = get_res_name(self.filename)
        self.refreshIndicatorObjects()

    def refreshIndicatorObjects(self):
        full_img_path = os.path.join(self.img_path, self.filename)
        full_gt_path = os.path.join(self.gt_path, self.gt_name)
        full_pred_path = os.path.join(self.pred_path, self.pred_name)
        self.edit_path.setText(full_img_path)
        self.edit_gt_path.setText(full_gt_path)
        self.QELogPath.setText(full_pred_path)



    def selectedFileChanged(self):
        par_p_i = self.edit_path.text().rfind('/')
        par_p = self.edit_path.text()[0:par_p_i]
        new_text = os.path.join(par_p, self.filelists.currentItem().text())
        self.filename = self.filelists.currentItem().text()
        self.gt_name = get_gt_name(self.filename)
        self.pred_name = get_res_name(self.filename)
        self.refreshIndicatorObjects()



    def refreshViews(self):
        if self.viewlists['img_view']:
            self.view_img.syncSelectItems(os.path.join(self.img_path, self.filename),os.path.join(self.gt_path, self.gt_name),os.path.join(self.pred_path, self.pred_name))
            self.refresh_image_view()


    #things about image view
    def open_image_view(self):
        self.view_img = Img_view_control.ImgViewContrl()
        self.view_img.view_closed.connect(self.close_image_view)
        self.view_img.show()
        self.viewlists['img_view'] = 1
        self.refresh_image_view()

    def close_image_view(self):
        print('img_view_closed')
        self.viewlists['img_view'] = 0

    def refresh_image_view(self):
        full_img_path = os.path.join(self.img_path, self.filename)
        full_gt_path = os.path.join(self.gt_path, self.gt_name)
        full_pred_path = os.path.join(self.pred_path, self.pred_name)
        self.view_img.refresh(full_img_path, full_gt_path, full_pred_path)

    def calPerformance(self):
        from script_test_ch4 import get_performance
        resDict = get_performance.get_performance(self.pred_path, gt_path=self.gt_path, res_path='./tmp/results.zip')
        result_str = get_performance.fomat_results(resDict)
        self.QResults.setText(result_str)

    def closeEvent(self, QCloseEvent):
        self.exit()





def getDirectory():
    fd = QtWidgets.QFileDialog()
    fd.setFileMode(fd.Directory)
    fd.setViewMode(fd.Detail)
    # fd.setNameFilter("Images(*.png *.jpg)")
    # choosed_path = fd.getExistingDirectory(self, "choose a directory", default_path, options=fd.ShowDirsOnly)
    if fd.exec_():
        choosed_path = fd.selectedFiles()
        return choosed_path[0]

def getFiles():
    fd = QtWidgets.QFileDialog()
    fd.setFileMode(fd.ExistingFiles)
    fd.setViewMode(fd.Detail)
    # fd.setNameFilter("Images(*.png *.jpg)")
    # choosed_path = fd.getExistingDirectory(self, "choose a directory", default_path, options=fd.ShowDirsOnly)
    if fd.exec_():
        choosed_path = fd.selectedFiles()
        return choosed_path

def get_short_name(filename):
    short_filename_i = filename.rfind('.')
    short_filename = filename[0:short_filename_i]
    return  short_filename

def get_gt_name(imgname):
    return  "gt_{}.txt".format(get_short_name(imgname))

def get_res_name(imgname):
    return  "res_{}.txt".format(get_short_name(imgname))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())