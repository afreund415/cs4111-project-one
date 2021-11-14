Readme steps for submission: 
    Submit a separate uncompressed README file on Gradescope with the following information:

    The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)

    The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

    A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

    Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.




Folder Structure:
    1. Schema for our DB (implemented on PSQL)
    2. Static for css stylesheet
    3. Templates with html pages. Super basic. 
    4. CSVs with csv data as it stands at the moment
    5. server.py where all the current python lives

Running: 
    Right now, all you have to do to run the program is switch to the folder, and run <python server.py --debug> and it'll run. The debug part is optional

Submitting pull requests on github:
    1. git pull 
    2. git add -A 
    3. git commit -m "message"
    4. git push 



Copying CSV Data into tables:
    Note: The order matters due to the constraints so if you're adding new data in bulk to a table, make sure you follow this order. You should also navigate to the CSV folder before you run psql in order for the copy and paste to work. 
    1. \copy Countries FROM './Countries.csv' with (format csv, header true, delimiter ',');
    2. \copy Risk_Groups FROM './Risk_Groups.csv' with (format csv, header true, delimiter ',');
    3. \copy Travelers FROM './Travelers.csv' with (format csv, header true, delimiter ',');
    4. \copy Policies FROM './Policies.csv' with (format csv, header true, delimiter ',');
    5. \copy Flies_To FROM './Flies_To.csv' with (format csv, header true, delimiter ',');
    6. \copy Member_Of FROM './Member_Of.csv' with (format csv, header true, delimiter ',');
    7. \copy Itineraries FROM './Itineraries.csv' with (format csv, header true, delimiter ',');



Installation:
   
Navigation: 

