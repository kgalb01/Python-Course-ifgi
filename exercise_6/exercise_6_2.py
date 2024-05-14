# Python in QGIS and ArcGIS
# Exercise 6, Task 2
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-14

from qgis.core import QgsVectorLayer, QgsField, QgsProject, edit
from qgis.PyQt.QtCore import QVariant

# Open the shapefiles, which contain the swimming pools and districts
# Note: The paths to the shapefiles may need to be adjusted based on the location of the files on your system
swimming_pools_layer = QgsVectorLayer('C:/Users/kgalb/Documents/Workspace/Python/data/exercise_6/Data for Session 6/public_swimming_pools.shp', 'public_swimming_pools', 'ogr')
districts_layer = QgsVectorLayer('C:/Users/kgalb/Documents/Workspace/Python/data/exercise_6/Muenster/Muenster_City_Districts.shp', 'Muenster_City_Districts', 'ogr')

# Check if the layers were loaded successfully
if not swimming_pools_layer.isValid():
    print("Failed to load swimming pool layer!")

if not districts_layer.isValid():
    print("Failed to load districts layer!")

# Get the index of the "Type" column in the swimming pool layer
type_field_index = swimming_pools_layer.fields().indexFromName('Type')

# Get the index of the "district" column in the swimming pool layer
district_field_index = swimming_pools_layer.fields().indexFromName('district')
if district_field_index == -1:
    # Add the "district" column if it doesn't exist
    swimming_pools_layer.dataProvider().addAttributes([QgsField('district', QVariant.String, len=50)])
    swimming_pools_layer.updateFields()  # Update fields to reflect the changes
    district_field_index = swimming_pools_layer.fields().indexFromName('district')

# Iterate over each swimming pool feature in the layer
swimming_pool_features = swimming_pools_layer.getFeatures()

# Modify the values in the "Type" column and add the "district" column
with edit(swimming_pools_layer):
    for swimming_pool_feature in swimming_pool_features:
        # Change the value in the "Type" column
        type_value = swimming_pool_feature.attributes()[type_field_index]
        if type_value == 'H':
            swimming_pool_feature.setAttribute(type_field_index, 'Hallenbad')
        elif type_value == 'F':
            swimming_pool_feature.setAttribute(type_field_index, 'Freibad')
        
        # Implement logic to identify the district for each swimming pool
        # Here, we perform a spatial query to determine the district
        for district_feature in districts_layer.getFeatures():
            if swimming_pool_feature.geometry().within(district_feature.geometry()):
                district_name = district_feature.attribute('Name')
                swimming_pool_feature.setAttribute(district_field_index, district_name)
                break  # Skip to the next district loop if the district is found
        
        # Save the changes
        swimming_pools_layer.updateFeature(swimming_pool_feature)

# Add the layer to the map
QgsProject.instance().addMapLayer(swimming_pools_layer)
