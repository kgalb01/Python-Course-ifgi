# Python in QGIS and ArcGIS
# Exercise 4, Task 1
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-05-04

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# Get the name of the district
district_name = "[%Name%]"

# Construct the URL for the Wikipedia page of the district
wikipedia_url = "https://en.wikipedia.org/wiki/" + district_name

# Create an instance of QWebView
web_view = QWebView()

# Load the Wikipedia page URL
web_view.load(QUrl(wikipedia_url))

# Show the QWebView window
web_view.show()
