# Python in QGIS and ArcGIS
# Exercise 8
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-14

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from .export_dialog import Ui_Export
from .exercise_7_10 import CreateCityDistrictProfile
from qgis.core import QgsProcessingFeedback

class ExportData(QDialog, Ui_Export):
    """
    A dialog window for exporting data.

    Args:
        district_name (str): The name of the district.
        iface (object): The interface object.

    Attributes:
        iface (object): The interface object.
        district_name (str): The name of the district.

    """

    def __init__(self, district_name, iface):
        super().__init__()
        self.iface = iface
        self.district_name = district_name
        self.setupUi(self)
        self.pushButton_pfd.clicked.connect(self.select_pdf_path)
        self.pushButton_csv.clicked.connect(self.select_csv_path)
        self.toolButton.clicked.connect(self.export_as_pdf)
        self.toolButton_2.clicked.connect(self.export_as_csv)
        self.pushButton.clicked.connect(self.accept)

    def select_pdf_path(self):
        """
        Opens a file dialog to select the PDF output path.

        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.lineEdit_pdf_outputpath.setText(file_path)

    def select_csv_path(self):
        """
        Opens a file dialog to select the CSV output path.

        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.lineEdit_csv_outputpath.setText(file_path)

    def export_as_pdf(self):
        """
        Exports the data as a PDF file.

        """
        file_path = self.lineEdit_pdf_outputpath.text()
        if not file_path:
            QMessageBox.warning(self, "No Path", "Please provide a file path for the PDF!")
            return

        profile = CreateCityDistrictProfile()
        profile.createPDF(self.district_name, file_path, QgsProcessingFeedback())
        QMessageBox.information(self, "Success", "PDF created successfully!")

    def export_as_csv(self):
        """
        Exports the data as a CSV file.

        """
        file_path = self.lineEdit_csv_outputpath.text()
        if not file_path:
            QMessageBox.warning(self, "No Path", "Please provide a file path for the CSV!")
            return

        profile = CreateCityDistrictProfile()
        profile.create_csv(self.district_name, file_path)
        QMessageBox.information(self, "Success", "CSV created successfully!")

    def get_selected_district(self):
        """
        Gets the selected district from the active layer.

        Returns:
            list: A list of selected district names.

        """
        selected_layer = self.iface.activeLayer()
        if selected_layer and selected_layer.name() == 'Muenster_City_Districts':
            selected_features = selected_layer.selectedFeatures()
            return [feature['Name'] for feature in selected_features]  
        return []
