# Python in QGIS and ArcGIS
# Exercise 6, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-14

import csv
import sys
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject
from qgis.PyQt.QtCore import QVariant

# Set the maximum integer value for the csv field size limit
maxInt = sys.maxsize
decrement = True

# Decrease the maximum integer value until the csv field size limit can be set
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

# Create a new empty vector layer in memory
layer = QgsVectorLayer("MultiPolygon?crs=epsg:4326", "temp_standard_land_value_muenster", "memory")

# Get the data provider for the layer
provider = layer.dataProvider()

# Define the fields for the layer
fields = [
    QgsField("standard", QVariant.Double),
    QgsField("type", QVariant.String),
    QgsField("district", QVariant.String)
]

# Add the fields to the layer
provider.addAttributes(fields)
layer.updateFields()

# Open the CSV file
# Note: The path to the file may need to be adjusted based on the location of the files on your system
with open('C:/Users/kgalb/Documents/Workspace/Python/data/exercise_6/Data for Session 6/standard_land_value_muenster.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)  # Skip the header row

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Create a new feature
        feature = QgsFeature()

        # Set the attributes for the feature
        feature.setAttributes([float(row[0].replace(',', '.')), row[1], row[2]])

        # Set the geometry for the feature
        feature.setGeometry(QgsGeometry.fromWkt(row[3]))

        # Add the feature to the layer
        provider.addFeature(feature)

# Update the layer extents
layer.updateExtents()

# Add the layer to the current project
QgsProject.instance().addMapLayer(layer)
