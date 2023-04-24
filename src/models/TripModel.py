import pandas as pd
from models.entities.TripEntity import TripEntity, Base
from database.db import get_session, get_engine, check_db_exists, execute_query, execute_select
from message.message_queue import update_status

#Columns expected in the CSV to load
EXPECTED_COL_NAMES = ['region','origin_coord','destination_coord','datetime','datasource']

#Class that contains the method to manipulate the Trips requirements through the API.
class TripModel():
    """
    Class Method to load the trips into database. After the load, it will call set_group_trips method.
    Params
        @self: Automatic filled by Python. Reference of the current instance of the class
        @path: String. route to the CSV to load
        @grouping_coordinate_degree: Float. Number that will be used to round coords and be able to get grouped
    Returns:
        Number of rows loaded
    """
    @classmethod
    def load_trips(self, path, grouping_coordinate_degree):
        try:
            update_status('CSV load process started', 0)
            #Start DB connection, check if database is created, then recreate tables in order to clean the environment.
            check_db_exists()
            Base.metadata.drop_all(get_engine())
            Base.metadata.create_all(get_engine())
            session = get_session()

            #Load CSV
            df = pd.read_csv(path)

            #Validations
            if len(df.columns) != len(EXPECTED_COL_NAMES):
                raise ValueError(f"Expected {len(EXPECTED_COL_NAMES)} columns but got {len(df.columns)}. Names of columns expected are {EXPECTED_COL_NAMES}")

            if not all(name in df.columns for name in EXPECTED_COL_NAMES):
                raise ValueError(f"Expected columns with names {EXPECTED_COL_NAMES} but got {df.columns.tolist()}")

            update_status('CSV is loading', 10)
            #Start loading trips into database.
            row_count = 0
            for row in df.iterrows():
                trip = TripEntity(
                    region=row['region'],
                    origin_coord=row['origin_coord'],
                    destination_coord=row['destination_coord'],
                    datetime=row['datetime'],
                    datasource=row['datasource'],
                    trip_group = ''
                )
                session.add(trip)
                row_count+=1
            session.commit()

            update_status('CSV has been loaded', 50)
            update_status('Grouping trips with a using {degree} to round coordinates'.format(degree = grouping_coordinate_degree), 51)

            #Call function set_group_trips to group trips by filling the field "trip_group" in trips table
            self.set_group_trips(grouping_coordinate_degree)

            update_status('Grouping trips has been completed', 99)
            update_status('Load has been completed', 100)
            return row_count
        except Exception as ex:
            update_status('An error ocurred: ' + ex, 0)
            raise ex
        
    """
    Class method to group the trips by using origin coordinate, destionation coordinate and hour. Origin and destination coordinates will be rounded using grouping_coordinate_degree.
    The value of the operation will be stored in column "trips_group" of the trips table.
    Params
        @self: Automatic filled by Python. Reference of the current instance of the class
        @grouping_coordinate_degree: Float. Number that will be used to round coords and be able to get grouped
    """
    @classmethod
    def set_group_trips(self, grouping_coordinate_degree):
        try:
            execute_query(get_session(), "call udp_update_trip_group(:degree)", {'degree': grouping_coordinate_degree})
        except Exception as ex:
            raise ex

    """
    Class method which will returns the groups of trips in which their quantity of trips more or equal that the minimum_count value given by parameter. This method also return the data for the trips 
    Params
        @self: Automatic filled by Python. Reference of the current instance of the class
        @minimum_count: Parameter to define the minimum quantity of trips that a group should have in order to be returned
    Return:
        Dictionary with the information grouped by trip.
    """
    @classmethod 
    def get_trips_grouped(self, minimum_count):
        try:
            session = get_session()
            result = execute_select(session, "select * from udf_get_trips_grouped(:minimum)", {'minimum': minimum_count} ).fetchall()
            df = pd.DataFrame(result)
            if df.empty:
                return 0
            else:
                grouped_df = df.groupby('trip_group').apply(lambda x: x.to_dict(orient='records')).to_dict()
                return grouped_df
        except Exception as ex:
            raise ex

    """
    Class method that will return the weekly average quantity of trips performed in a region
    Params
        @self: Automatic filled by Python. Reference of the current instance of the class
        @region: Name of the region where the trips should be filtered and get the average.
    Return:
        Dictionary with the information grouped by week.
    """
    @classmethod 
    def get_weekly_average_trips_by_region(self, region):
        try:
            session = get_session()
            result = execute_select(session, 
                                    "select * from udf_get_weekly_average_trips_by_region(:pregion)", 
                                    {'pregion': region})
            df = pd.DataFrame(result.fetchall())
            if df.empty:
                return 0
            else:
                weekly_avg = df.groupby("week_year").mean()["num_trips"].reset_index().to_dict(orient='records')
                return weekly_avg
        except Exception as ex:
            raise ex
        
    
    """
    Class method that will return the weekly average quantity of trips performed in a bounding box
    Params
        @self: Automatic filled by Python. Reference of the current instance of the class
        @bounding_box: Coords in the order of (minlongitude, minlatitude, maxlongitude, maxlatitude). By using this, the calculation will take the trips in which the travel goes through the given coords.
    Return:
        Dictionary with the information grouped by week.
    """
    @classmethod 
    def get_weekly_average_trips_by_bbox(self, bounding_box):
        try:
            session = get_session()
            arr_bounding = bounding_box.replace('(', '').replace(')', '').split(',')
            result = execute_select(session, 
                                    "select * from udf_get_weekly_average_trips_by_bbox(:minlon, :minlat, :maxlon, :maxlat)", 
                                    {'minlon': arr_bounding[0], 'minlat': arr_bounding[1], 'maxlon': arr_bounding[2], 'maxlat': arr_bounding[3]})
            df = pd.DataFrame(result.fetchall())
            if df.empty:
                return 0
            else:
                weekly_avg = df.groupby("week_year").mean()["num_trips"].reset_index().to_dict(orient='records')
                return weekly_avg
        except Exception as ex:
            raise ex
        

