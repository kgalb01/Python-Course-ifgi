# Python in QGIS and ArcGIS
# Exercise 9, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-19

import arcpy

# Set the workspace to the geodatabase
# Might need to be adjusted to the correct path
arcpy.env.workspace = r"C:/Users/kgalb/Documents/Workspace/ArcGIS/exercise_9/exercise_arcpy_1.gdb"

# set counter for active assets to 0
active_assets_count = 0

# function to create output file
def output(fc):
    # if active_assets exists, delete it
    if arcpy.Exists("active_assets"):
        arcpy.Delete_management("active_assets")
    # else create active_assets with the same schema as the input feature class
    arcpy.CreateFeatureclass_management(arcpy.env.workspace,"active_assets","POINT",fc,fc,fc)

# iterate over all feature classes in the geodatabase
for fc in arcpy.ListFeatureClasses():
    desc = arcpy.Describe(fc) # get the description of the feature class to get properties
    # print the name and shape type of the feature class
    # this is just for testing purposes, might delete later
    # print(f"Feature class: {desc.name}, Shape type: {desc.shapeType}") 
    
    # if-clause to check if the shape of the iterated feature is type "Point"
    if desc.shapeType == "Point":
        
        # if-clause to check if the output feature class already exists
        if not arcpy.Exists("active_assets"):
            # create the output feature class
            output(fc)
        
        # create search cursor
        with arcpy.da.SearchCursor(fc, ["SHAPE@", "status"]) as search_cursor:
            
            # create insert cursor to write to the output feature class
            with arcpy.da.InsertCursor("active_assets", ["SHAPE@", "status"]) as insert_cursor:
                
                # iterate over all rows in the search cursor
                for row in search_cursor:
                    
                    # Check whether the point has the attribute "active"
                    if row[1] == 'active':
                        
                        # If the point is active, insert it into the output feature class
                        insert_cursor.insertRow(row)
                        
                        # increment a counter for each active asset
                        active_assets_count += 1

# print success message
print(f"Active assets added to active_assets: {active_assets_count}")
