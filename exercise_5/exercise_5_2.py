# Python in QGIS and ArcGIS
# Exercise 5, Task 2
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-14

from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsPointXY
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtWidgets import QInputDialog, QMessageBox

# Getting user input for coordinates
parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text="51.96066, 7.62476")

if bOK:
    try:
        lat, lon = map(float, sCoords.split(','))
    except ValueError:
        iface.messageBar().pushMessage("Error", "Invalid coordinates format. Please enter latitude and longitude separated by comma.", level=QgsMessageBar.CRITICAL)
        exit()
else:
    exit()

# Creating the coordinate transformation from WGS84 to ETRS89 32N
crs_wgs84 = QgsCoordinateReferenceSystem('EPSG:4326')  # WGS84
crs_etrs89_32n = QgsCoordinateReferenceSystem('EPSG:25832')  # ETRS89 32N
xform = QgsCoordinateTransform(crs_wgs84, crs_etrs89_32n, QgsProject.instance())
transformed_point = xform.transform(lon, lat)

# Checking if the transformed coordinates fall within a district of Münster
layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
point = QgsPointXY(transformed_point)
for feature in layer.getFeatures():
    if feature.geometry().contains(point):
        QMessageBox.information(None, "Geoguesser Result", f"The coordinates fall within the district of {feature['Name']}.")
        break
else:
    QMessageBox.information(None, "Geoguesser Result", "The coordinates do not fall within any district of Münster.")
