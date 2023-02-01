import json
from shapely.geometry import shape, Point, Polygon, MultiPolygon

def simplify_geojson(input_file, output_file, area_threshold):
    with open(input_file, 'r') as f:
        geojson = json.load(f)

    features = geojson['features']
    simplified_features = []

    for feature in features:
        geometry = feature['geometry']
        if geometry['type'] == 'Polygon':
            polygon = Polygon(geometry['coordinates'][0])
            simplified_polygon = polygon.simplify(area_threshold, preserve_topology=False)
            if isinstance(simplified_polygon, Polygon) and simplified_polygon.area > 0:
                simplified_coordinates = [[list(x) for x in simplified_polygon.exterior.coords]]
                simplified_geometry = {'type': 'Polygon', 'coordinates': simplified_coordinates}
                simplified_features.append({'type': 'Feature', 'geometry': simplified_geometry, 'properties': feature['properties']})
        elif geometry['type'] == 'MultiPolygon':
            simplified_polygons = []
            for polygon in geometry['coordinates']:
                polygon = Polygon(polygon[0])
                simplified_polygon = polygon.simplify(area_threshold, preserve_topology=False)
                if isinstance(simplified_polygon, Polygon) and simplified_polygon.area > 0:
                    simplified_polygons.append([[list(x) for x in simplified_polygon.exterior.coords]])
            simplified_geometry = {'type': 'MultiPolygon', 'coordinates': simplified_polygons}
            simplified_features.append({'type': 'Feature', 'geometry': simplified_geometry, 'properties': feature['properties']})
        else:
            print(f'{geometry["type"]} is not supported.')
            return

    simplified_geojson = {'type': 'FeatureCollection', 'features': simplified_features}

    with open(output_file, 'w') as f:
        json.dump(simplified_geojson, f)

input_file = 'CourtMap.geojson'
output_file = 'CourtMapSimple.geojson'
area_threshold = 0.0101

simplify_geojson(input_file, output_file, area_threshold)
