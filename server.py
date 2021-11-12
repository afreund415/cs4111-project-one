import os
import functools
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, flash, render_template, g, redirect, Response, session, url_for
import psycopg2
# delete before submission 
from decouple import config #tool for hiding uri credentials 


app = Flask(__name__)   
# The secret key is necessary for the session stuff to work...
# need to look up if this is something we should dynamically create or not 
app.secret_key = 'dev'
#uri = config('uri', default='')
#uri = "postgresql://andreasfreund:1234@localhost/dbproj1"
uri = "postgresql://acf2175:6901@34.74.246.148/proj1part2"
engine = create_engine(uri)

# ensures that the database is connected before requests
@app.before_request
def before_request():
    try: 
        g.conn = engine.connect()

    except:
        print("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None

# closes db connection after requests
@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

# passes the traveler_id to other views...enables our "logged-in" code to work
@app.before_request
def load_existing_traveler():
    tid = session.get('tid')

    if tid is None:
        g.user = None
    else:
        g.user= g.conn.execute(
            "SELECT * FROM travelers WHERE traveler_id = '{}'".format(tid)).fetchone()
    
# function that allows you to restrict views only to existing travelers
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # this needs better error handling
        if g.user is None:
            # return redirect(url_for('auth.login'))
            return "something went wrong"
        return view(**kwargs)   

    return wrapped_view
        

# homepage that shows generic list of travelers
# this should be changed dramatically 
@app.route('/')
def index():
    
    # Not sure we need any of this in the long run...best to just format the page 
    # print (request.args)
    # cur = g.conn.execute("SELECT * From travelers")
    # travelers = []
    # for r in cur:
    #     travelers.append(r)
    # cur.close()
    # context = dict(data = travelers)

    # return render_template("index.html", **context)
    return render_template("index.html")



# add new traveler
@app.route('/add', methods=['POST'])
def add():
    fname = request.form['fname']
    lname = request.form['lname']
    vax_status = request.form['vax_status']
    citizenship = request.form['citizenship']
    dob = request.form['dob']
    # email = request.form['email']
    error = None

    if (not fname) or (not lname):
       error = "Please provide both your first and last names" 

    elif not vax_status:
        error = "Your vaccination status is required"
    
    elif not citizenship:
        error = "Please provide your citizenship"

    elif not dob: 
        error = "Please provide your date of birth"

    if error is None:
        try:
            g.conn.execute(
                """INSERT INTO travelers(fname, lname, vax_status, citizenship, dob)
                VALUES (%s,%s,%s,%s,%s)""", (fname, lname, vax_status, citizenship, dob)
            )
            # gets recently added traveler_id
            # All the work below to actually get a recently added traveler ID feels dumb to me. 
            # There must be a better way to do this but works for now
            cur = g.conn.execute(
                """SELECT traveler_id FROM travelers WHERE fname = '{}' AND lname = '{}'
                AND vax_status = '{}' AND citizenship = '{}' AND dob = '{}' 
                """.format(fname, lname, vax_status, citizenship, dob)
            )
            if cur.rowcount > 0 and cur.rowcount < 2:
                for r in cur:
                    newtid = r[0].strip()
                cur.close()

                # adds the recently created traveler's credentials to their session...for logged-in view
                session.clear()
                session['tid'] = newtid
                # redirects to the create trip page with recently created travel id
                return redirect(url_for('trip', tid = newtid))
            else: 
                error = "Could not create traveler"
        except Exception as e:
            error = type(e) + " " + e.args
    # asks traveler to try again if not successful 
    flash(error)
    return render_template("index.html")



# page for addding a new trip...requires an existing traveler_id
@app.route('/trip/<tid>', methods=('GET', 'POST')) 
@login_required
def trip(tid):
    
    return render_template("newtrip.html")


# add new itinerary
@app.route('/addtrip', methods=['POST'])
def addtrip():
    country_id_origin = request.form['country_id_origin']
    country_id_destination = request.form['country_id_destination']
    travel_date = request.form['travel_date']
    departure_time = request.form['departure_time']
    # calls helper function to find correct policy for origin-destination pair
    policy_id = findPolicy(country_id_origin, country_id_destination)
    # gets traveler_id from session 
    traveler_id = session['tid']
    error = None

    # make sure that origin-dest pair are already in flies_to so we don't crash
    if (not country_id_origin) or (not country_id_destination):
       error = "Please provide an origin and destiniation country" 

    elif not travel_date:
        error = "Please include a travel date for your trip"
    
    elif not policy_id:
        error = "Could not locate a policy for this trip"

    elif not traveler_id: 
        error = "Traveler id could not be found"    

    # SQL for inserting the intinerary
    if error is None:
        try:
            g.conn.execute(
                """INSERT INTO itineraries(country_id_origin, country_id_destination, policy_id,
                traveler_id, travel_date, departure_time) VALUES (%s,%s,%s,%s,%s,%s)""", 
                (country_id_origin, country_id_destination, policy_id, 
                traveler_id, travel_date, departure_time)
            )
            # get recently-added trip policy
            pName = ''
            pURL = ''
            pRiskGroup = ''
            cur = g.conn.execute(
                "SELECT * FROM policies WHERE policy_id = '{}'".format(policy_id)
            )
            if cur.rowcount > 0 and cur.rowcount < 2:
                for r in cur: 
                    pName = r['pname']
                    pUrl = r['policy_data']
                    pRiskGroup = r['group_id']
                cur.close()
                # builds temp link to policy page
                hyperlink_format = '<a href="{link}">{text}</a>'
                link = hyperlink_format.format(link = pUrl, text = pName + ' Policy Link')
        
                # temporary string to show traveler their newly-added trip's policy 
                responseStr = """For your trip on {}  from {}  to {},  the 
                    following Covid-19 policy applies: {}""".format(travel_date, 
                    country_id_origin, country_id_destination, link)

                # we will need an HTML template for this eventually 
                return (responseStr)
            else:
                error = "Could not create a new trip"
        except Exception as e:
            error = type(e) + " " + e.args
    # asks traveler to try again if not successful 
    flash(error)
    return redirect(url_for('trip', tid = session['tid']))

# helper method for finding policy for an origin-destination pair
def findPolicy(origin, dest):
    # creates a list of the riskgroup ids for each policy that a destination-country uses
    destRiskGroups = [] 
    cur = g.conn.execute(
        "SELECT * FROM policies WHERE country_id = '{}'".format(dest)
    )
    for r in cur: 
        destRiskGroups.append(r['group_id']) 
    cur.close
    # uses a helper method to find out which riskgroup the origin falls into
    group_id = getGroup(destRiskGroups, origin)

    # if it gets a riskgroup id, we can now select the correct policy and return the policy id
    if group_id != null:
        cur2 = g.conn.execute(
            """SELECT policy_id FROM policies WHERE country_id = '{}' 
            AND group_id = '{}'""".format(dest, group_id)
        )
    # not robust: doesn't check to make sure that cur2 only has 1 element...
    for r in cur2: 
        pid = r['policy_id']
    cur2.close()

    return pid

    # else:
        # need some sort of error handling here w/ alternative return statement
        # Maybe just return NULL that way the error is passed along and handled in addTrip method

# helper method for finding correct risk group for an origin-dest pair 
# takes a list of destination's policies' riskgroups, and finds out which 
# one applies to the origin country 
def getGroup(destRiskGroups, origin):
    # error = None
    if (len(destRiskGroups) != 0):
        for riskGroup in destRiskGroups:
            
            cur = g.conn.execute(
                """SELECT group_id FROM Member_Of WHERE country_id = '{}' 
                AND group_id = '{}'""".format(origin, riskGroup)
            )
        if cur.rowcount >= 0: # Changed > to >=
            return riskGroup
    # else:
        # what should we do here?
        # Maybe just return NULL that way the error is passed along and handled in addTrip method

# hello world page
@app.route('/hello')
def hello():
    return 'Hello, World!'

# main function that runs the entire app 
if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='localhost')
    @click.argument('PORT', default=5000, type=int)
    
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(debug=debug, threaded=threaded)

    run()







 

# SCRAP CODE FOR TESTING STUFF BELOW!

# @app.route('/policies', methods=('GET', 'POST'))
# def policies():
#     cur = g.conn.execute("SELECT pname FROM policies")
#     names = []

#     for result in cur:
#         names.append(result['pname'])
#     cur.close()
#     return names

# adds variable to url which is the travelerID...we can use this for seeing a 
# traveler's itineraries for instance

@app.route('/traveler/<tid>', methods=['GET', 'POST'])
def showTraveler(tid):
    cur = g.conn.execute("SELECT * FROM itineraries WHERE traveler_id='{}'".format(tid)) 

    trips = []

    for r in cur:
        trips.append(r)
    
    cur.close()
    context = dict(data = trips)
    return render_template("itineraries.html", **context)



