# The json module is needed to load the geoJSON file
import json
# The shapefile, from pyshp, is needed to construct the shapefile object
import shapefile

class GeoJ:

    geometryType = ''
    columnsList = []
    __attributesPerF = []
    attributes = []
    geometries = []

    shpFileObj = None
    
    # The constructor which basically needs the geoJSON file+path as an argument
    def __init__(self, geoJFile):
        # This try statement makes sure that the geojson file exists and it is in JSON structure
        try:
            self.geoJFile = open(geoJFile)
        except IOError:
            print "Error: can not find file. Make sure the file name and path are correct"
        else:
            try:
                self.geoJObj = json.load(self.geoJFile)
            except ValueError:
                print("Error: the file is not in JSON structure")
            else:
                # If everything is fine, the __parseGeoJ private method will 
                # collect attributes and geometries from the geoJSON file
                self.__parseGeoJ()

    def __parseGeoJ(self):

        self.geometryType = self.geoJObj['features'][0]['geometry']['type']

        self.columnsList = self.geoJObj['features'][0]['properties'].keys()

        for i in self.geoJObj['features']:

            if i['geometry']['type'] == self.geometryType:
                self.geometries.append(i['geometry']['coordinates'])
                for j in self.columnsList:
                    self.__attributesPerF.append(str(i['properties'][str(j)]))
                self.attributes.append(self.__attributesPerF)
                self.__attributesPerF = []

    # This method along with the following private methods will create a shapefile
    # from the collected attributes and geometries from the geoJSON file
    def toShp(self, shpFile):

        if self.geometryType == 'Point':
            self.__createPoint()
        elif self.geometryType == 'LineString':
            self.__createLine()
        elif self.geometryType == 'Polygon':
            self.__createPolygon()
        else:
            print('Can not proceed. The geometry type ' + self.geometryType + ' is not supported in this program')
            return

        # Calling the __createPrjFile method to create a .prj file
        self.__createPrjFile(shpFile)

        # Saving the shape file, which creates .shp, .shx, and .dbf files
        self.shpFileObj.save(shpFile)

    # This method is used to create points shapefile
    def __createPoint(self):

        self.shpFileObj = shapefile.Writer(shapefile.POINT)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.point(i[0],i[1])

        for j in self.attributes:
            self.shpFileObj.record(*j)
    
    # This method is used to create lines shapefile
    def __createLine(self):

        self.shpFileObj = shapefile.Writer(shapefile.POLYLINE)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.line(parts=[i])

        for j in self.attributes:
            self.shpFileObj.record(*j)

    # This method is used to create polygons shapefile
    def __createPolygon(self):

        self.shpFileObj = shapefile.Writer(shapefile.POLYGON)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.poly(parts=i)

        for j in self.attributes:
            self.shpFileObj.record(*j)

    # This method is used to create the columns names read from the geoJSON file
    def __createColumns(self):

        for i in self.columnsList:
            # Field names cannot be unicode.
            # That is why I cast it to string.
            self.shpFileObj.field(str(i), 'C', '50')

    # This method currently creates a .prj file with WGS84 projection
    def __createPrjFile(self, shpFile):

        prjFile = open( shpFile + '.prj', 'w')
        prjStr = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        prjFile.write(prjStr)
        prjFile.close()

##########################
#      running main      #
##########################

if __name__ == '__main__':

    # Create an object from the GeoJ class
    gJ = GeoJ('input/lines.geojson')
    
    # Creating a shapefile from the geoJSON object
    gJ.toShp('output/lines')
