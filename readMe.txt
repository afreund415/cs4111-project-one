Readme steps for submission: 
    Submit a separate uncompressed README file on Gradescope with the following information:

    The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)

    The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

    A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

    Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

Description: 
For part 3 of our project, we decided to take the web front-end option. As stated in our proposal, we built
an application that provides international travelers with current COVID-19 policies related to their trips.
Through the use of multiple SQL queries, travelers are able to interact with our database by inputting basic
traveler and trip information and recieving the corresponding COVID-19 policy that applies to their itinerary.
As mentioned in our proposal, we aggregated policy data by hand from government travel department websites.
Currently, our database has policy data for over 30 destination countries and can support more than 1800
origin-destination pairs. In addition to our original proposal, we added a unique email attribute which was
used to support multiple trips by the same traveler.

Two pages:
The first of the two web pages that requires some of the more interesting database operations is our "New Traveler"
page (/add). On this page, travelers input their identifying information to include name, email, date of birth,
citizenship, and vaccination status. The citizenship input is a dropdown menu which uses a SELECT query that
interacts with the countries table to list all the countries found in our database. The traveler's input goes
through an error handling process before it reaches an INSERT query which passes the information into the database
and stores it in the travelers table. Following this, a SELECT query is used alongside the traveler's email to
obtain the corresponding unique traveler_id attribute associated with the traveler. The traveler_id is passed into
a URL that is used to keep track of a traveler's trips in the following pages.

The second of the two web pages that requires some of the more interesting database operations is our "New Trip"
page (/addtrip). On this page, travelers input their itinerary details to include origin, destination, travel date,
and time. The destination input is a dropdown menu which uses a SELECT statement that interacts with the policies
and countries tables to produce the destinations that are supported. The origin and destination attributes are then 
passed into a helper method that uses multiple SELECT queries on the policies table to identify if the database
supports this trip, and if it does, it produces a policy_id attribute. The policy_id, along with the traveler's
input, goes through an error handling process before it reaches an INSERT query which passes the information into
the database and stores it in the iteneraries table. Finally, if the trip is supported by the database, a SELECT
query is used to produce and output the policy URL which corresponds to the traveler's trip.


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


