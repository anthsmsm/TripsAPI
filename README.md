#Prerequisites

The system will requiere python 3.11 properly installed and postgresql with the extension postgis created, or postgis's docker image.

Steps to execute:

1)Create the destination folder where the project will be located or use GIT clone inside it to get the project or directly download from github and decompress it. I nmy case, the folder that will contain the project will be C:\Projects

git clone https://github.com/anthsmsm/TripsAPI.git

![Imagen1](https://user-images.githubusercontent.com/131601602/233890507-412a7e74-929b-486e-9887-1400cd9d2621.jpg)

2)In this section, we will use postgis's docker image to run a postgresql database. In order to do that, please install and configure properly Docker Desktop. Once it is installed, open the command line and run the following command:

docker run --name postgisdb  -p 5432:5432 -e POSTGRES_USER=sa -e POSTGRES_PASSWORD=SuperStrongP4ssw0rd -d postgis/postgis 

3) With any IDE for database administration that can connect to POSTGRESQL (like DBeaver), connect to postgresql server (default database postgres), create the database "python_rest_api" or open a new SQL Script and execute the following command:
CREATE DATABASE python_rest_api;

4) After the database is created, connect to it, open the script "init.sql" that can be found in the root directory of the downloaded project from GIT, and execute it.

5) Open a command line window and set the directory to the root path of the downloaded project.

6)You can skip to next step, but it is good this app runs in a virtual environment. To create a virtual enviroment for the python project. Replace {path} with the folder where the project is located and {name_venv} with the name of the virtual environment.
python -m venv {path}\{name_venv}

Then activate the virtual environment by calling the env\Scripts\activate or env\Scripts\activate.bat file.
env\Scripts\activate.bat

7) In command line, go to the folder path where the requirements.txt file is, and run the following command, which will install all the dependencies of the project:
pip install -r requirements.txt


8) Please set the parameters in .env file according to the proper values of the postgresql database configured in step 2

SECRET_KEY=P4SSW0R1*_?
SQL_HOST=localhost
SQL_USER=sa
SQL_PASSWORD=SuperStrongP4ssw0rd
SQL_DATABASE=python_rest_api
SQL_PORT=5432

9) Execute src/app.py
python src\app.py

