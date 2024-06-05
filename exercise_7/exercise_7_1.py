# Python in QGIS and ArcGIS
# Exercise 7, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-05

import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFileDestination,
                       QgsVectorLayer,
                       QgsGeometry,
                       QgsDistanceArea,
                       QgsProject)
from qgis import processing
from qgis.utils import iface
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    """
    This is an example algorithm that creates a PDF profile for a city district. 
    We are interested in the parent districts, area size, number of households and number of plots. 
    We also distinguish between schools and public swimming pools for each query and count the number of the selected feature in a district. 
    """
    
    INPUT = 'INPUT'
    City_District = 'CITY_DISTRICT'
    Type = 'TYPE'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateCityDistrictProfile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createCityDistrictProfile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Custom Scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'customscripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr('Creates a PDF profile for a selected city district in Münster.')
    
    def __init__(self):
        """
        Constructor of the class that initializes our layer variables.
        """
        super().__init__()
        self.district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        self.muenster_parcel = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0]
        self.house_numbers = QgsProject.instance().mapLayersByName('House_Numbers')[0]
        

    def initAlgorithm(self, config=None):
        #This method defines the inputs and outputs of the algorithm
        self.addParameter(
            QgsProcessingParameterEnum(
                self.City_District, 'City District', options=self.get_names_from_district()
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.Type, 'Select one Option for Information', options=['Schools', 'Public Swimming Pools']
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output PDF'), 
                fileFilter='PDF-Data (*.pdf)'
            )
        )

    # This method returns a list of city district names sorted from a-z
    # It retrieves the names from the “Münster_Stadtteile” level.
    def get_names_from_district(self):
        district = [feature['Name'] for feature in self.district_layer.getFeatures()]
        return sorted(district)

    
    '''This method creates a PDF profile of our selected district.
    It contains the name of the district, the parent district, the size of the area, the number of households, the number of plots 
    and the number of selected facilities (schools or swimming pools).
    In addition, it should provide a map image of the district of interest, which is used to create the pdf.
    We have used the following source for help'''
        
    #https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
    def createPDF(self, district_name, type_choice, output_path, feedback):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        c.setLineWidth(.3)
        c.setFont('Helvetica', 12)

        c.drawString(100, height - 100, "City District Profile: " + district_name)
        c.drawString(100, height - 140, "Parent District: " + self.parent_district(district_name))
        c.line(100, height - 145, 500, height - 145)
    
        c.drawString(100, height - 180, "Area size: " + str(self.calculate_area(district_name)) + " km²")
        c.line(100, height - 185, 500, height - 185)
    
        c.drawString(100, height - 220, "Number of Households: " + str(self.get_feature_count(district_name, 'house_numbers')))
        c.line(100, height - 225, 500, height - 225)
    
        c.drawString(100, height - 260, "Number of Parcels: " + str(self.get_feature_count(district_name, 'muenster_parcel')))
        c.line(100, height - 265, 500, height - 265)
    
        if type_choice == 'Schools':
            count = self.get_feature_count(district_name, 'facilities', 'Schools')
            if count > 0:
                c.drawString(100, height - 300, "Number of Schools: " + str(count))
            else:
                c.drawString(100, height - 300, "No schools in this district")
        else:
            count = self.get_feature_count(district_name, 'facilities', 'public_swimming_pools')
            if count > 0:
                c.drawString(100, height - 300, "Number of Public Swimming Pools: " + str(count))
            else:
                c.drawString(100, height - 300, "No public swimming pools in this district")
        c.line(100, height - 325, 500, height - 325)
    
        #https://stackoverflow.com/questions/2422798/python-os-path-join-on-windows
        picture_district = os.path.join(os.path.dirname(output_path), 'feature.png')
        self.create_map_image(district_name, picture_district, feedback)
        c.drawImage(picture_district, 100, height - 500, width=400, height=200)


        c.showPage()
        c.save()


    '''
    This method returns the name of the parent district for the selected city district.
    It retrieves the name of the parent district from the 'Muenster_City_Districts' layer. 
    This function has the same approach as get_names_from_district
    '''
    def parent_district(self, district_name):
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                return feature['P_District']
        return "Unknown"
        
    '''
    We use this function to calculate our area size of the district selected by the user.
    We use the geometry methods and the 'ETRS89' ellipsoid for an even more accurate measurement than if we were to do it alternatively.
    The area is displayed in the unit square kilometer rounded to two decimal places.
    We working with the our solution from task 5 
    '''

    def calculate_area(self, district_name):
        selected_district = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                selected_district = feature
                break
        
        if selected_district is None:
            raise QgsProcessingException("City district '" + district_name + "' not found.")
        
        geom = selected_district.geometry()

        da = QgsDistanceArea()
        da.setEllipsoid("ETRS89")
        
        crs = QgsProject.instance().crs()
        transform_context = QgsProject.instance().transformContext()
        da.setSourceCrs(crs, transform_context)

        area = round(da.measureArea(geom) / 1e6, 2) 
        return area

    '''
    This method returns the number of specified features (households, parcels or facilities) within the selected district.
    We work here with the geometry of the district to find out if the features are included in the area 
    '''
    def get_feature_count(self, district_name, feature_type, layer_name=None):
        district_geom = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                district_geom = feature.geometry()
                break

        if district_geom is None:
            raise QgsProcessingException("City district '" + district_name + "' not found.")

        if feature_type == 'house_numbers':
            feature_layer = self.house_numbers
        elif feature_type == 'muenster_parcel':
            feature_layer = self.muenster_parcel
        elif feature_type == 'facilities':
            feature_layer = QgsProject.instance().mapLayersByName(layer_name)[0] if layer_name else None
            if not feature_layer:
                raise QgsProcessingException("Layer '" + layer_name + "' not found.")
        else:
            raise QgsProcessingException("Invalid'" + feature_type + "'.")
    
        #Counts the selected type, based on the geometry, whether it is contained in the selected district 
        count = 0
        for feature in feature_layer.getFeatures():
            if district_geom.contains(feature.geometry()):
                count += 1
        return count

    '''
    Here we create an image based on our city district, which we filter using the id to zoom in on it.
    The map view is then saved. We working with the information from the task and from the link.
    '''
    #https://gis.stackexchange.com/questions/231446/pyqgis-make-screenshot-of-mapcanvas-after-setextent-is-called
    def create_map_image(self, district_name, picture_district, feedback):
        # Find the feature ID of the selected district
        feature_id = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                feature_id = feature.id()
                break

        if feature_id is None:
            feedback.reportError("City district '" + district_name + "' not found, no map created.")
            return

        # Zoom to the feature ID of the selected district
        iface.mapCanvas().zoomToFeatureIds(self.district_layer, [feature_id])

        while iface.mapCanvas().isDrawing():
            time.sleep(5)
            
        # Save the map image
        iface.mapCanvas().saveAsImage(picture_district)
        feedback.pushInfo("Map image saved to " + picture_district)

    def processAlgorithm(self, parameters, context, feedback):
        """
        This function executes the algorithm by retrieving the necessary parameters,
        determining the district name and dataset choice, and calling the createPDF function.
        """
        dist_index = self.parameterAsEnum(parameters, self.City_District, context)
        type_index = self.parameterAsEnum(parameters, self.Type, context)
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        

        district_name = self.get_names_from_district()[dist_index]
        type_choise = ['Schools', 'Public Swimming Pools'][type_index]
        
    
        self.createPDF(district_name, type_choise, output_path, feedback)
        return {self.OUTPUT: output_path}
