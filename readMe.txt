Folder Structure:
    1. Schema for our DB (implemented on PSQL)
    2. Static for css stylesheet
    3. Templates with html pages. Super basic. 
    4. CSVs with csv data as it stands at the moment
    5. server.py where all the current python lives

Running: 
    Right now, all you have to do to run the program is switch to the folder, and run <python server.py --debug> and it'll run. The debug part is optional

Copying CSV Data into tables:
    Note: The order matters due to the constraints so if you're adding new data in bulk to a table, make sure you follow this order. You should also navigate to the CSV folder before you run psql in order for the copy and paste to work. 
    1. \copy Countries FROM './Countries.csv' with (format csv, header true, delimiter ',');
    2. \copy Risk_Groups FROM './Risk_Groups.csv' with (format csv, header true, delimiter ',');
    3. \copy Travelers FROM './Travelers.csv' with (format csv, header true, delimiter ',');
    4. \copy Policies FROM './Policies.csv' with (format csv, header true, delimiter ',');
    5. \copy Flies_To FROM './Flies_To.csv' with (format csv, header true, delimiter ',');
    6. \copy Member_Of FROM './Member_Of.csv' with (format csv, header true, delimiter ',');
    7. \copy Itineraries FROM './Itineraries.csv' with (format csv, header true, delimiter ',');


Hernan was here 11/7 @ 6:15pm
WEB-APP

Installation:
   

Running CLI: 



