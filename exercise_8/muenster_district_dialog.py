# Python in QGIS and ArcGIS
# Exercise 8
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-14

from PyQt5.QtWidgets import QDialog
from .muenster_base import Ui_muensterCityDistrictToolsDialogBase

class muensterCityDistrictToolsDialog(QDialog, Ui_muensterCityDistrictToolsDialogBase):
    def __init__(self, parent=None):
        """
        Constructor for the muensterCityDistrictToolsDialog class.

        Args:
            parent: The parent widget (default: None).
        """
        super(muensterCityDistrictToolsDialog, self).__init__(parent)
        self.setupUi(self)  # Initialize the UI

        # Check if the buttonBox attribute exists
        if not hasattr(self, 'button_box'):
            raise AttributeError('button_box is not defined in the UI file')

