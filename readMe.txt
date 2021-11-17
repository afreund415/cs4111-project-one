Readme steps for submission: 
    Submit a separate uncompressed README file on Gradescope with the following information:

    The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)

    The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

    A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

    Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

Description: 

Two pages:


URL: http://35.243.131.10:8111/
PSQL: The PostgreSQL account is under Andreas’ UNI (acf2175)

Structure: 
    1. Schema folder (not used dynamically) with our DB Schema design
    2. server.py file where all the SQL queries and website backend logic lives
    3. Templates folder with HTML templates for webpages
    4. Static folder with our CSS stylesheet
    5. CSVs folder with latest version of hard-coded data for our DB (Policies, Risk_Groups, Member_Of, and Flies_To)

Running: 
    In correct folder with proper packages installed, <run python server.py --debug>


