# Python in QGIS and ArcGIS
# Exercise 5, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-14

from qgis.core import QgsProject, QgsFeatureRequest, QgsGeometry
from PyQt5.QtWidgets import QInputDialog, QMessageBox

def schools_districts():
    # Access to our individual layers
    distance_calculator = QgsDistanceArea()
    districts_muenster_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
    schools_muenster_layer = QgsProject.instance().mapLayersByName('Schools')[0]

    # Extract and sort names from the individual districts
    # http://www.qgistutorials.com/en/docs/getting_started_with_pyqgis.html
    district = [f['Name'] for f in districts_muenster_layer.getFeatures()]
    district.sort()

    # Selection option for the user, who can view and select the districts
    parent = iface.mainWindow()
    selected_district, ok = QInputDialog.getItem(parent, "Select District", "Districts:", district, 0, False)

    # If the selection is canceled, a QMessageBox appears, i.e. a window where a warning message is displayed
    if not ok:
        QMessageBox.warning(parent, "Selection was Cancelled", "No district has been selected!!")
        return

    # FilterRequest
    district_filter = QgsFeatureRequest().setFilterExpression(f"\"Name\" = '{selected_district}'")

    # Fetches the next object from the iteration of features. If there are no more features, none is output
    district_feature = next(districts_muenster_layer.getFeatures(district_filter), None)

    # Find the center of the district
    # https://stackoverflow.com/questions/39897203/get-a-centroid-in-qgis-via-python
    centroid_from_district = district_feature.geometry().centroid()

    # Prepare distance calculation, ETRS89 our CRS
    # https://gis.stackexchange.com/questions/347802/calculating-elipsoidal-length-of-line-in-pyqgis
    distance_calculator.setEllipsoid('ETRS89')

    # With this function, we check whether a school is located in the selected district. To help us with this, we have used the contains() function.
    # If we then know which schools are located within a district, we calculate the distance to the center of the district with the class QgsDistanceArea 
    # and its function measureLine()
    # https://gis.stackexchange.com/questions/347702/calculate-distance-from-a-point-to-a-multilinestring-geometry-pyqgis
    # https://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/geometry.html
    schools_muenster = []
    for school in schools_muenster_layer.getFeatures():
        if district_feature.geometry().contains(school.geometry()):
            distance = distance_calculator.measureLine(school.geometry().asPoint(), centroid_from_district.asPoint())
            distance_km = round(distance / 1000, 2)
            schools_muenster.append(f"{school['Name']}, Distance: {distance_km} km")

    # Display the found schools and their distances
    # Line break: https://www.python-forum.de/viewtopic.php?t=41566
    if schools_muenster:
        schools_z = "\n".join(schools_muenster)
        QMessageBox.information(parent, f"Schools in {selected_district}", schools_z)
    else:
        QMessageBox.information(parent, "Result", "No schools found in the selected district.")

# Run function
schools_districts()
