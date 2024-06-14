# Python in QGIS and ArcGIS
# Exercise 7, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-06-14

import csv
import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterEnum, QgsProcessingParameterFileDestination,
                       QgsVectorLayer, QgsGeometry, QgsDistanceArea, QgsProject,
                       QgsProcessingFeedback)
from qgis.utils import iface
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    City_District = 'CITY_DISTRICT'
    Type = 'TYPE'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateCityDistrictProfile()

    def name(self):
        return 'createCityDistrictProfile'

    def displayName(self):
        return self.tr('Create City District Profile')

    def group(self):
        return self.tr('Custom Scripts')

    def groupId(self):
        return 'customscripts'

    def shortHelpString(self):
        return self.tr('Creates a PDF profile for a selected city district in Münster.')

    def __init__(self):
        super().__init__()
        self.district_layer = None
        self.muenster_parcel = None
        self.house_numbers = None

        self.init_layers()

    def init_layers(self):
        try:
            self.district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
            self.muenster_parcel = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0]
            self.house_numbers = QgsProject.instance().mapLayersByName('House_Numbers')[0]
        except IndexError:
            raise Exception("Required layers are not loaded. Please load 'Muenster_City_Districts', 'Muenster_Parcels', and 'House_Numbers'.")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum(self.City_District, 'City District', options=self.get_names_from_district()))
        self.addParameter(QgsProcessingParameterEnum(self.Type, 'Select one Option for Information', options=['Schools', 'Public Swimming Pools']))
        self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT, self.tr('Output PDF'), fileFilter='PDF-Data (*.pdf)'))

    def get_names_from_district(self):
        self.district_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')
        if not self.district_layer:
            raise Exception("Layer 'Muenster_City_Districts' not found.")
        self.district_layer = self.district_layer[0]
        district = [feature['Name'] for feature in self.district_layer.getFeatures()]
        return sorted(district)

    def createPDF(self, district_name, output_path, feedback):
        if feedback is None:
            feedback = QgsProcessingFeedback()

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

        school_count = self.get_feature_count(district_name, 'facilities', 'Schools')
        if school_count > 0:
            c.drawString(100, height - 300, "Number of Schools: " + str(school_count))
            c.line(100, height - 305, 500, height - 305)
        else:
            c.drawString(100, height - 300, "No schools in this district")
            c.line(100, height - 305, 500, height - 305)

        pool_count = self.get_feature_count(district_name, 'facilities', 'public_swimming_pools')
        if pool_count > 0:
            c.drawString(100, height - 340, "Number of Public Swimming Pools: " + str(pool_count))
        else:
            c.drawString(100, height - 340, "No public swimming pools in this district")

        c.line(100, height - 370, 500, height - 370)


        c.showPage()
        c.save()

       
        
        

    def parent_district(self, district_name):
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                return feature['P_District']
        return "Unknown"

    def calculate_area(self, district_name):
        selected_district = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                selected_district = feature
                break

        if selected_district is None:
            raise Exception("City district '" + district_name + "' not found.")

        geom = selected_district.geometry()

        da = QgsDistanceArea()
        da.setEllipsoid("ETRS89")

        crs = QgsProject.instance().crs()
        transform_context = QgsProject.instance().transformContext()
        da.setSourceCrs(crs, transform_context)

        area = round(da.measureArea(geom) / 1e6, 2)
        return area

    def get_feature_count(self, district_name, feature_type, layer_name=None):
        district_geom = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                district_geom = feature.geometry()
                break

        if district_geom is None:
            raise Exception("City district '" + district_name + "' not found.")

        if feature_type == 'house_numbers':
            feature_layer = self.house_numbers
        elif feature_type == 'muenster_parcel':
            feature_layer = self.muenster_parcel
        elif feature_type == 'facilities':
            feature_layer = QgsProject.instance().mapLayersByName(layer_name)[0] if layer_name else None
            if not feature_layer:
                raise Exception("Layer '" + layer_name + "' not found.")
        else:
            raise Exception("Invalid'" + feature_type + "'.")

        count = 0
        for feature in feature_layer.getFeatures():
            if district_geom.contains(feature.geometry()):
                count += 1
        return count

    def create_map_image(self, district_name, picture_district, feedback):
        feature_id = None
        for feature in self.district_layer.getFeatures():
            if feature['Name'] == district_name:
                feature_id = feature.id()
                break

        if feature_id is None:
            feedback.reportError("City district '" + district_name + "' not found, no map created.")
            return

        iface.mapCanvas().zoomToFeatureIds(self.district_layer, [feature_id])

        while iface.mapCanvas().isDrawing():
            time.sleep(5)

        iface.mapCanvas().saveAsImage(picture_district)
        feedback.pushInfo("Map image saved to " + picture_district)

    def processAlgorithm(self, parameters, context, feedback):
        self.muenster_parcel = QgsProject.instance().mapLayersByName('Muenster_Parcels')
        self.house_numbers = QgsProject.instance().mapLayersByName('House_Numbers')

        if not self.muenster_parcel:
            raise Exception("Layer 'Muenster_Parcels' not found.")
        if not self.house_numbers:
            raise Exception("Layer 'House_Numbers' not found.")

        self.muenster_parcel = self.muenster_parcel[0]
        self.house_numbers = self.house_numbers[0]

        dist_index = self.parameterAsEnum(parameters, self.City_District, context)
        type_index = self.parameterAsEnum(parameters, self.Type, context)
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        district_name = self.get_names_from_district()[dist_index]
        type_choise = ['Schools', 'Public Swimming Pools'][type_index]

        self.createPDF(district_name, type_choise, output_path, feedback)
        return {self.OUTPUT: output_path}

    def get_district_info(self, district_name):
        schools = self.get_feature_count(district_name, 'facilities', 'Schools')
        pools = self.get_feature_count(district_name, 'facilities', 'public_swimming_pools')
        return schools, pools

    'https://www.python-lernen.de/csv-datei-einlesen.htm'
    def create_csv(self, district_name, file_path):
        with open(file_path, 'w') as csv_file:
            csv_file.write("District Name, Size, Number of Parcels, Number of Schools\n")
            size = self.calculate_area(district_name)
            parcels = self.get_feature_count(district_name, 'muenster_parcel')
            schools = self.get_feature_count(district_name, 'facilities', 'Schools')
            csv_file.write(str(district_name) + ", " + str(size) + ", " + str(parcels) + ", " + str(schools) + "\n")
