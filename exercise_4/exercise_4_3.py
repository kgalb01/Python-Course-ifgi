# Python in QGIS and ArcGIS
# Exercise 4, Task 3
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-06

import os
from qgis.core import QgsVectorLayer, QgsProject

# Define the path to the Münster folder
muenster_folder = r"C:/Users/kgalb/Documents/Workspace/Python/data/exercise_4/Muenster"

# Get a list of all files in the Münster folder
shapefiles = [file for file in os.listdir(muenster_folder) if file.endswith('.shp')]

# Create a new QGIS instance and load the project
project = QgsProject.instance()
project.setTitle('myFirstProject')

# Iterate through the shapefiles and add them to the project
for shapefile in shapefiles:
    # Construct the full path to the shapefile
    shapefile_path = os.path.join(muenster_folder, shapefile)
    
    # Create the layer
    layer = QgsVectorLayer(shapefile_path, os.path.splitext(shapefile)[0], "ogr")
    
    # Check if the layer is valid
    if layer.isValid():
        # Add the layer to the project
        project.addMapLayer(layer)
        print(f"Layer '{os.path.splitext(shapefile)[0]}' has been added to the project.")
    else:
        print(f"Error loading layer '{os.path.splitext(shapefile)[0]}'.")

# Save the project
project_path = r"C:/Users/kgalb/Documents/Workspace/Python/data/exercise_4/myFirstProject.qgz"
project.write(project_path)
print(f"Project saved as 'myFirstProject' at: {project_path}")
