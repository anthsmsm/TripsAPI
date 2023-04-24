Prerequisites:

The system will requiere python 3.11 properly installed and postgresql with the extension postgis created, or postgis's docker image.

--------------------------------------------------------------------------
Steps to execute:

1) Create the destination folder where the project will be located or use GIT clone inside it to get the project or directly download from github and decompress it. I nmy case, the folder that will contain the project will be C:\Projects

git clone https://github.com/anthsmsm/TripsAPI.git

![Imagen1](https://user-images.githubusercontent.com/131601602/233890507-412a7e74-929b-486e-9887-1400cd9d2621.jpg)

2) In this section, we will use postgis's docker image to run a postgresql database. In order to do that, please install and configure properly Docker Desktop. Once it is installed, open the command line and run the following command:

docker run --name postgisdb  -p 5432:5432 -e POSTGRES_USER=sa -e POSTGRES_PASSWORD=SuperStrongP4ssw0rd -d postgis/postgis 

![image](https://user-images.githubusercontent.com/131601602/233890924-c93cc9a1-6a00-4296-864f-327004417c05.png)

3) With any IDE for database administration that can connect to POSTGRESQL (like DBeaver), connect to postgresql server (default database postgres), create the database "python_rest_api" or open a new SQL Script and execute the following command:
CREATE DATABASE python_rest_api;
![image](https://user-images.githubusercontent.com/131601602/233891087-33755a2e-b899-40ee-b060-0d095759d5bf.png)

4) After the database is created, connect to it, open the script "init.sql" that can be found in the root directory of the downloaded project from GIT, and execute it.
![image](https://user-images.githubusercontent.com/131601602/233891234-c4dbc111-fc55-496c-896f-4bab34972930.png)

5) Back to the command line window of step one, set "TripsAPI" as root flder
![image](https://user-images.githubusercontent.com/131601602/233891385-9bbcf64a-133a-40f1-af7e-b0ebe2a8d871.png)

6) You can skip to next step, but it is good this app runs in a virtual environment. To create a virtual enviroment for the python project. Replace {name_venv} with the name of the virtual environment, in my case it will be env.
python -m venv {name_venv}
![image](https://user-images.githubusercontent.com/131601602/233891666-28e2ad93-f7d4-4536-b8b4-2f38a54a8681.png)

Then activate the virtual environment by calling the env\Scripts\activate or env\Scripts\activate.bat file.
env\Scripts\activate.bat
![image](https://user-images.githubusercontent.com/131601602/233891712-2db21231-75d3-41ec-9df3-885f56958d2f.png)

7) In command line, go to the folder path where the requirements.txt file is, and run the following command, which will install all the dependencies of the project:
pip install -r requirements.txt
![image](https://user-images.githubusercontent.com/131601602/233891822-5b0349bf-030d-4120-86f0-824dc63db8cc.png)

8) Please set the parameters in .env file according to the proper values of the postgresql database configured in step 2. The default values are:

SECRET_KEY=P4SSW0R1*_?
SQL_HOST=localhost
SQL_USER=sa
SQL_PASSWORD=SuperStrongP4ssw0rd
SQL_DATABASE=python_rest_api
SQL_PORT=5432

9) Execute src/app.py
python src\app.py
![image](https://user-images.githubusercontent.com/131601602/233892528-ade6eae8-5ba5-4f9b-a9c0-240a002efbda.png)

--------------------------------------------------------------------------

Test

This RestfulAPI contains four POST method and one websocket

1) load
Load the data from the CSV and group the trips by origin coords, destionation coords and hour (it calls the same function as set_trips_grouped method), this last value is store in the column trip_group from trips table.
Params in JSON:
   @path: String. Route where the CSV is located.
   @grouping_coords_degree: Float. Number that will be used to round coords and be able to get grouped. If not defined, 0.5 will be used. Take in mind that 0.1 degree equals to 11KM.
JSON Example:
{
	"path":"https://drive.google.com/uc?id=14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU"
	, "grouping_coords_degree": 0.5
}
http://127.0.0.1:5000/trips/load
![image](https://user-images.githubusercontent.com/131601602/233895235-d1acee05-e4cf-40e9-b677-756fb0e58b8e.png)

2) get_trips_grouped
Returns the groups of trips in which their quantity of trips more or equal that the minimum_count value given by parameter. This method also return the data for the trips
Param in JSON:
    @minimum_count: Parameter to define the minimum quantity of trips that a group should have in order to be returned
JSON Example:
{
	"minimum_count":2
}
http://127.0.0.1:5000/trips/get_trips_grouped
![image](https://user-images.githubusercontent.com/131601602/233895218-cb6333f7-7d7a-46e6-b055-c805d7707501.png)

3)set_trips_grouped
Group the trips by origin coords, destionation coords and hour in the trips table.
Params in JSON:
   @grouping_coords_degree: Float. Number that will be used to round coords and be able to get grouped. If not defined, 0.5 will be used. Take in mind that 0.1 degree equals to 11KM.
JSON Example:
{
	"grouping_coord_degree":0.5
}
http://127.0.0.1:5000/trips/set_trips_grouped
![image](https://user-images.githubusercontent.com/131601602/233895302-d65859aa-99bb-4c15-806b-0e272cc898ea.png)

4)weekly_average_trips
Return the weekly average quantity of trips performed in a region or in a bouncing box. If both are settend, only region will be used.
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
http://127.0.0.1:5000/trips/weekly_average_trips
![image](https://user-images.githubusercontent.com/131601602/233895454-cc94416e-db0a-4cfb-a5f4-a611a6ed0b46.png)
![image](https://user-images.githubusercontent.com/131601602/233895426-ae2cdf45-5881-461f-99b3-63a7ace756f1.png)


Server will message to all clients connected about the status of the ingestion through the POST Method load.
![image](https://user-images.githubusercontent.com/131601602/233895726-6d3260e9-3220-44a9-b314-3975b27f4157.png)

------------------------------------------------------------------------------
The file Answer_to_questions.sql contains the select statements to the answer to the following question

-From the two most commonly appearing regions, which is the latest datasource?
-What regions has the "cheap_mobile" datasource appeared in?

------------------------------------------------------------------------------
Sketch up in cloud

Azure BLOB Storage/Azure DataLake: Utilize a blob storage location as a landing place where the file will be received and will trigger an Azure DAta Factory process to start the ingestion.
Azure Data Factory: With this tool, the file received can be processed and loaded into Azure SQL Database, also additional process can be performed over the data after the ingestion, in order to have it ready to be consumed by RestAPI.
Azure SQL Database: Database to store up the data ingested
Azure Events Hubs: As a message broker.
Azure Functions: To integrate a restapi application that will, mainly, return inquiries over the data processed

--------------------------------------------------------------------------------

