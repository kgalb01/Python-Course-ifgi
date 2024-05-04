# Python in QGIS and ArcGIS
# Exercise 4, Task 2
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-04-05

from qgis.PyQt.QtCore import QFileInfo

# Open CSV file
# Adjust the path to the file if necessary
with open('C:/Users/kgalb/Documents/Workspace/Python/data/exercise_4/Muenster/SchoolReport.csv', 'w') as file:
    # Write the header of the CSV file
    file.write('Name;X;Y\n')
    
    # Check if a selected feature exists
    if len(iface.activeLayer().selectedFeatures()) > 0:
        
        # Iterate through all selected features
        for selected_feature in iface.activeLayer().selectedFeatures():
            
            # Extract the name of the school
            school_name = selected_feature['Name']
            
            # Replace special characters in the school name
            # This step is optional but the .csv file couldn't represent the special characters properly
            school_name = school_name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
            
            # Extract the X and Y coordinates from the geometry
            geometry = selected_feature.geometry()
            x_coord = geometry.asPoint().x()
            y_coord = geometry.asPoint().y()
            
            # Write the information to the CSV file
            file.write(f'{school_name};{x_coord};{y_coord}\n')
    else:
        print('No selected feature available.')
