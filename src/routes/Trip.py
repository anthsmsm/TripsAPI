from flask import Blueprint, jsonify, request
from models.TripModel import TripModel
import re

main = Blueprint('trips_blueprint', __name__)
"""
Post method to load the data from the CSV and group the trips by origin coords, destionation coords and hour (it calls the same function as set_trips_grouped method), this last value is store in the column trip_group from trips table.
Params in JSON:
   @path: String. Route where the CSV is located.
   @grouping_coords_degree: Float. Number that will be used to round coords and be able to get grouped. If not defined, 0.5 will be used. Take in mind that 0.1 degree equals to 11KM.
JSON Example:
{
	"path":"https://drive.google.com/uc?id=14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU"
	, "grouping_coords_degree": 0.5
}
"""
@main.route('/load', methods=['POST'])
def load_trips():
    try:
        result = TripModel.load_trips(request.json['path'], request.json.get('grouping_coords_degree', 0.5))
        if result > 0:
            return jsonify({'message': '{number} from CSV has been loaded into database'.format(number = result)}), 200
        else:
            return jsonify({'message': '0 rows has been loaded'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

"""
Post method that returns the groups of trips in which their quantity of trips more or equal that the minimum_count value given by parameter. This method also return the data for the trips
Param in JSON:
    @minimum_count: Parameter to define the minimum quantity of trips that a group should have in order to be returned
JSON Example:
{
	"minimum_count":2
}
"""
@main.route('/get_trips_grouped', methods=['POST'])
def get_trips_grouped():
    try:
        minimum_count = request.json.get('minimum_count', 2)
        result = TripModel.get_trips_grouped(minimum_count)
        if (result == 0):
            return jsonify({'message': 'No trip groups has more than {count} trips'.format(count = minimum_count)}), 200
        else:
            return jsonify(result), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
"""
Post method to group the trips by origin coords, destionation coords and hour in the trips table.
Params in JSON:
   @grouping_coords_degree: Float. Number that will be used to round coords and be able to get grouped. If not defined, 0.5 will be used. Take in mind that 0.1 degree equals to 11KM.
JSON Example:
{
	"grouping_coord_degree":0.5
}
"""    
@main.route('/set_trips_grouped', methods=['POST'])
def set_trips_grouped():
    try:
        degree = request.json.get('grouping_coord_degree', 0.5)
        result = TripModel.set_group_trips(degree)
        return jsonify({'message': 'Trips has been grouped by origin, destination and hour, using a degreee rounding of {d}'.format(d = degree)}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
"""
Post method that will return the weekly average quantity of trips performed in a region or in a bouncing box. If both are settend, only region will be used.
Params in JSON:
    @region: Name of the region where the trips should be filtered and get the average.
    @bounding_box: Coords in the order of (minlongitude, minlatitude, maxlongitude, maxlatitude). By using this, the calculation will take the trips in which the travel goes through the given coords.
JSON Example 1:
{
	"region": "Hamburg"
}
JSON Example 2
{
	"bounding_box": "(9.849758,53.530411,9.991550,53.606563)"
	
}
"""    
@main.route("/weekly_average_trips", methods=['POST'])
def weekly_average_trips():
    try:
        region = request.json.get("region", '')
        bbox = request.json.get("bounding_box", '')
        result = ''
        if region != '':
            result = TripModel.get_weekly_average_trips_by_region(region)
        elif bbox != '':
            if not re.search(r"^\(", bbox):
                bbox = '(' + bbox
            if not re.search(r"\)$", bbox):
                bbox = bbox + ')'
            if not re.match(r"\(\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+\)", bbox):
                result = {"message": "The bounding box pattern required is min longitude, min latitude, max longitude, max latitude. For example 9.849758,53.530411,9.991550,53.606563"}
            else:    
                result = TripModel.get_weekly_average_trips_by_bbox(bbox)
        else:
            result = {"message": "Region or bounding box values needs to be provided"}
        return jsonify(result), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
