# Python in QGIS and ArcGIS
# Exercise 9, Task 2
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-19

import arcpy

# Set the workspace to the geodatabase
# Might need to be adjusted to the correct path
arcpy.env.workspace = r"C:/Users/kgalb/Documents/Workspace/ArcGIS/exercise_9/exercise_arcpy_1.gdb"

# Python commands directly copied from Buffer Toolbox in ArcGIS Pro
# As per this Video Tutorial: https://www.youtube.com/watch?v=sCkVI4VHdXo
# Then merged into feature class 'coverage'

# 300 meter buffer around masts
arcpy.analysis.Buffer(
in_features=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\masts",
out_feature_class=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\masts_Buffer_300m",
buffer_distance_or_field="300 Meters",
line_side="FULL",
line_end_type="ROUND",
dissolve_option="ALL",
dissolve_field=None,
method="PLANAR"
)

print(f"Buffering of masts completed.")

# 50 meter buffer around mobile antennas
arcpy.analysis.Buffer(
in_features=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\mobile_antennas",
out_feature_class=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\mobile_antennas_50m",
buffer_distance_or_field="50 Meters",
line_side="FULL",
line_end_type="ROUND",
dissolve_option="ALL",
dissolve_field=None,
method="PLANAR"
)

print(f"Buffering of mobile antennas completed.")


# 100 meter buffer around building antennas
arcpy.analysis.Buffer(
in_features=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\building_antenna",
out_feature_class=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\building_antenna_100m",
buffer_distance_or_field="100 Meters",
line_side="FULL",
line_end_type="ROUND",
dissolve_option="ALL",
dissolve_field=None,
method="PLANAR"
)

print(f"Buffering of mobile building antennas completed.")


# function to create a template buffer as in the buffering tool in ArcGIS Pro
def create_buffer(in_features, out_feature_class, buffer_distance):
    arcpy.analysis.Buffer(
        in_features=in_features,
        out_feature_class=out_feature_class,
        buffer_distance_or_field=buffer_distance,
        line_side="FULL",
        line_end_type="ROUND",
        dissolve_option="ALL",
        dissolve_field=None,
        method="PLANAR"
    )

# Iterate over the 'active_assets' feature class and create buffers based on the 'type' field
with arcpy.da.SearchCursor("active_assets", ['type']) as search_cursor:
    for row in search_cursor:
        
        if row[0] == 'mast':
            create_buffer("active_assets", r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\masts_Buffer_300m", "300 Meters")
            
        elif row[0] == 'mobile_antenna':
            create_buffer("active_assets", r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\mobile_antennas_50m", "50 Meters")
            
        elif row[0] == 'building_antenna':
            create_buffer("active_assets", r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\building_antenna_100m", "100 Meters")

# Merge the three buffer feature classes into one feature class
arcpy.management.Merge(
    inputs=[r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\masts_Buffer_300m", r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\mobile_antennas_50m", r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\building_antenna_100m"],
    output=r"C:\Users\kgalb\Documents\Workspace\ArcGIS\exercise_9\exercise_arcpy_1.gdb\coverage"
)

# print success message
print(f"All Buffers merged into 'coverage' feature class.")
