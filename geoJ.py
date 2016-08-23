import json
import shapefile

class GeoJ:

    geometryType = ''
    columnsList = []
    __attributesPerF = []
    attributes = []
    geometries = []

    shpFileObj = None

    def __init__(self, geoJFile):

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

        # Create the prj file in WGS84
        self.__createPrjFile(shpFile)

        # Save the shape file
        self.shpFileObj.save(shpFile)

    def __createPoint(self):

        self.shpFileObj = shapefile.Writer(shapefile.POINT)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.point(i[0],i[1])

        for j in self.attributes:
            self.shpFileObj.record(*j)

    def __createLine(self):

        self.shpFileObj = shapefile.Writer(shapefile.POLYLINE)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.line(parts=[i])

        for j in self.attributes:
            self.shpFileObj.record(*j)

    def __createPolygon(self):

        self.shpFileObj = shapefile.Writer(shapefile.POLYGON)
        self.shpFileObj.autoBalance = 1
        self.__createColumns()

        for i in self.geometries:
            self.shpFileObj.poly(parts=i)

        for j in self.attributes:
            self.shpFileObj.record(*j)

    def __createColumns(self):

        for i in self.columnsList:
            # Field names cannot be unicode.
            # That is why I cast it to string.
            self.shpFileObj.field(str(i), 'C', '50')

    def __createPrjFile(self, shpFile):

        prjFile = open( shpFile + '.prj', 'w')
        prjStr = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        prjFile.write(prjStr)
        prjFile.close()

##########################
#      running main      #
##########################

if __name__ == '__main__':

    gJ = GeoJ('input/lines.geojson')

    gJ.toShp('output/lines')