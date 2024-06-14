# Python in QGIS and ArcGIS
# Exercise 8
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-14

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 muensterCityDistrictTools
                                 A QGIS plugin
 Solution for the exercise 8.1
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-06-11
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jonas Starke / Kieran Galbraith
        email                : jstarke@uni-muenster.de / k_galb01@uni-muenster.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# muenster_district.py
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QApplication, QDialog
from qgis.core import QgsProject
from .resources import *
from .muenster_district_dialog import muensterCityDistrictToolsDialog
from .district_information_dialog import SecondDialog
from .export_dialog_data import ExportData
from .exercise_7_10 import CreateCityDistrictProfile
import os.path

class muensterCityDistrictTools:
    """QGIS Plugin Implementation.

    This class represents the implementation of a QGIS plugin for Muenster City District Tools.
    It provides various functionalities for working with district data in QGIS.

    Attributes:
        iface (QgsInterface): An interface instance that provides the hook by which you can manipulate the QGIS application at run time.
        plugin_dir (str): The directory path of the plugin.
        translator (QTranslator): The translator object for handling translations.
        actions (list): A list of QAction objects representing the actions of the plugin.
        menu (str): The name of the menu for the plugin.
        first_start (bool): A flag indicating if the plugin was started for the first time in the current QGIS session.
    """

    def __init__(self, iface):
        """Constructor.

        Args:
            iface (QgsInterface): An interface instance that will be passed to this class which provides the hook by which you can manipulate the QGIS application at run time.
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'muensterCityDistrictTools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Muenster City District Tools')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        Args:
            message (str, QString): String for translation.

        Returns:
            QString: Translated version of message.
        """
        return QCoreApplication.translate('muensterCityDistrictTools', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        Args:
            icon_path (str): Path to the icon for this action. Can be a resource path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
            text (str): Text that should be shown in menu items for this action.
            callback (function): Function to be called when the action is triggered.
            enabled_flag (bool, optional): A flag indicating if the action should be enabled by default. Defaults to True.
            add_to_menu (bool, optional): Flag indicating whether the action should also be added to the menu. Defaults to True.
            add_to_toolbar (bool, optional): Flag indicating whether the action should also be added to the toolbar. Defaults to True.
            status_tip (str, optional): Optional text to show in a popup when mouse pointer hovers over the action.
            whats_this (str, optional): Optional text to show in the status bar when the mouse pointer hovers over the action.
            parent (QWidget, optional): Parent widget for the new action. Defaults None.

        Returns:
            QAction: The action that was created. Note that the action is also added to self.actions list.
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/muenster_district/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Muenster City District Tools'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Muenster City District Tools'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Check if required layers are loaded
        if not self.check_required_layers():
            QMessageBox.critical(None, "Error", "Required layers are not loaded. Load 'Muenster_City_Districts', 'Muenster_Parcels', 'House_Numbers', 'Schools', and 'public_swimming_pools'.")
            return

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = muensterCityDistrictToolsDialog()
            self.dlg.toolButton_2.clicked.connect(self.show_information_dialog)
            self.dlg.toolButton.clicked.connect(self.export_data_from_feature)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass

    def check_required_layers(self):
        """Check if required layers are loaded."""
        required_layers = ['Muenster_City_Districts', 'Muenster_Parcels', 'House_Numbers', 'Schools', 'public_swimming_pools']
        loaded_layers = [layer.name().replace(' ', '') for layer in QgsProject.instance().mapLayers().values()]
        required_layers_sanitized = [layer.replace(' ', '') for layer in required_layers]
        for layer in required_layers_sanitized:
            if layer not in loaded_layers:
                return False
        return True

    def show_information_dialog(self):
        selected_district = self.get_selected_district()
        if selected_district:
            self.info_dialog = SecondDialog(selected_district)
            self.info_dialog.show()
            self.info_dialog.exec()
        else:
            QMessageBox.warning(self.dlg, "No Selection", "Please select a district!")

    def export_data_from_feature(self):
        selected_district = self.get_selected_district()
        if selected_district:
            self.export_dialog = ExportData(selected_district, self.iface)
            self.export_dialog.finished.connect(self.export_dialog.close)            
            self.export_dialog.exec()
        else:
            QMessageBox.warning(self.dlg, "No Selection", "Please select a district!")
        return

    def get_selected_district(self):
        selected_layer = self.iface.activeLayer()
        if selected_layer and selected_layer.name() == 'Muenster_City_Districts':
            selected_features = selected_layer.selectedFeatures()
            if selected_features:
                return selected_features[0]['Name']  # Assuming 'Name' is the attribute with district name
        return None
