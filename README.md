# geoJSONToShpFile
This code converts GeoJSON to shape files.
Please keep in mind that the current code expects the common geoJSON format with features list. The code will not work if you do not have the features list. The following example is OK since it has a features list with three points. One more important comment, shapefiles can hold only one feature type e.g. points, lines, and polygons. For that, I decided that the code will grab only features similar to the first feature in the list. In geoJSON, you can have different feature types in one feature list, and that does not work with shape files.

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {"id": 1,
                     "name": "Indian Ocean"
                    },
      "geometry": {
        "type": "Point",
        "coordinates": [
          80.15625,
          -22.91792293614602
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {"id": 2,
                     "name": "Atlantic Ocean"
                    },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -37.96875,
          17.644022027872726
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {"id": 3,
                     "name": "Pacific Ocean"
                    },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -164.1796875,
          1.4061088354351594
        ]
      }
    }
  ]
}
