# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'muenster_district_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_muensterCityDistrictToolsDialogBase(object):
    def setupUi(self, muensterCityDistrictToolsDialogBase):
        muensterCityDistrictToolsDialogBase.setObjectName("muensterCityDistrictToolsDialogBase")
        muensterCityDistrictToolsDialogBase.resize(400, 300)
        self.button_box = QtWidgets.QDialogButtonBox(muensterCityDistrictToolsDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.toolButton = QtWidgets.QToolButton(muensterCityDistrictToolsDialogBase)
        self.toolButton.setGeometry(QtCore.QRect(80, 170, 241, 31))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(muensterCityDistrictToolsDialogBase)
        self.toolButton_2.setGeometry(QtCore.QRect(80, 110, 241, 31))
        self.toolButton_2.setObjectName("toolButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(muensterCityDistrictToolsDialogBase)
        self.textBrowser.setGeometry(QtCore.QRect(40, 10, 181, 31))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(muensterCityDistrictToolsDialogBase)
        self.button_box.accepted.connect(muensterCityDistrictToolsDialogBase.accept) # type: ignore
        self.button_box.rejected.connect(muensterCityDistrictToolsDialogBase.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(muensterCityDistrictToolsDialogBase)

    def retranslateUi(self, muensterCityDistrictToolsDialogBase):
        _translate = QtCore.QCoreApplication.translate
        muensterCityDistrictToolsDialogBase.setWindowTitle(_translate("muensterCityDistrictToolsDialogBase", "Muenster City District Tools"))
        self.toolButton.setText(_translate("muensterCityDistrictToolsDialogBase", "Export data from the selected feature"))
        self.toolButton_2.setText(_translate("muensterCityDistrictToolsDialogBase", "Get data from the selected feature"))
        self.textBrowser.setHtml(_translate("muensterCityDistrictToolsDialogBase", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Muenster City District Tools</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))