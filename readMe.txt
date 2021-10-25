Super simple initial api with two endpoints


Folder Structure:
    1. Hello world python file with flask 
    2. Schema folder for SQL Schema
    3. CSVs folder for data dumps

Copying CSV Data into tables:
    Note: The order matters due to the constraints so if you're adding new data in bulk to a table, make sure you follow this order. You should also navigate to the CSV folder before you run psql in order for the copy and paste to work. 
    1. - \copy Countries FROM './Countries.csv' with (format csv, header true, delimiter ',');
    2. \copy Risk_Groups FROM './Risk_Groups.csv' with (format csv, header true, delimiter ',');
    3. \copy Travelers FROM './Travelers.csv' with (format csv, header true, delimiter ',');
    4. \copy Policies FROM './Policies.csv' with (format csv, header true, delimiter ',');
    5. \copy Flies_To FROM './Flies_To.csv' with (format csv, header true, delimiter ',');
    6. \copy Member_Of FROM './Member_Of.csv' with (format csv, header true, delimiter ',');
    7. \copy Itineraries FROM './Itineraries.csv' with (format csv, header true, delimiter ',');







WEB-APP

Installation:
    1. Flask: 
    https://flask.palletsprojects.com/en/2.0.x/installation/#install-flask
    2. Flask-RESTful: 
    https://flask-restful.readthedocs.io/en/latest/installation.html#installation


Running CLI: 
    1. Navigate to directory:
    2. Run in terminal: <python api.py>

Navigation: 
    1. To see get endpoint, go to http://127.0.0.1:5000/ and http://127.0.0.1:5000/api/get
    2. To try out post, do the following command in terminal: 
        <curl http://127.0.0.1:5000/api/post -H 'Content-Type: application/json' -d '{"name": "Andreas"}'> 
    Note: you can replace "Andreas" with any name


That's it! More very soon :) 

