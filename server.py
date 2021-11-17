import os
import functools
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import NullPool
from flask import Flask, request, flash, render_template, g, redirect, Response, session, url_for
import psycopg2
import secrets

app = Flask(__name__)   

# The secret key is necessary for the session management
app.secret_key = secrets.token_urlsafe(16)
# connects to our PSQL DB
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
        if g.user is None:
            return "something went wrong"
        return view(**kwargs)   
    return wrapped_view
        

# homepage that allows traveler to sign up 
@app.route('/')
def index():
    cur = g.conn.execute("SELECT * FROM countries ORDER BY cname")
    return render_template("index.html", cur = cur)
# add new traveler
@app.route('/add', methods=['POST'])
def add():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    vax_status = request.form['vax_status']
    citizenship = request.form['citizenship']
    dob = request.form['dob']
    error = None

    if (not fname) or (not lname):
       error = "Please provide both your first and last names" 
    elif not email:
        error = "Please provide an email"
    elif not vax_status:
        error = "Your vaccination status is required"  
    elif not citizenship:
        error = "Please provide your citizenship"
    elif not dob: 
        error = "Please provide your date of birth"
    else:
        cur = g.conn.execute(
            "SELECT * FROM travelers WHERE email = '{}'".format(email)
        )
        if cur.rowcount > 0:
            error = 'This email already exists' 
        cur.close()
    if error is None:
        try:
            g.conn.execute(
                """INSERT INTO travelers(fname, lname, email, vax_status, citizenship, dob)
                VALUES (%s,%s,%s,%s,%s,%s)""", (fname, lname, email, vax_status, citizenship, dob)
            )
            cur = g.conn.execute(
                "SELECT traveler_id FROM travelers WHERE email = '{}'".format(email)
            )
            for r in cur:
                # grabs new traveler_id
                newtid = r[0].strip()
            cur.close()
            # adds the recently created traveler's credentials to their session for logged-in view
            session.clear()
            session['tid'] = newtid
            # redirects to the create trip page with recently created travel id
            return redirect(url_for('trip', tid = newtid))
        except IntegrityError as e:
            pass
    # asks traveler to try again if not successful 
    flash(error)
    cur = g.conn.execute("SELECT * FROM countries ORDER BY cname")
    return render_template("index.html", cur = cur)



# page for addding a new trip...requires an existing traveler_id
@app.route('/trip/<tid>', methods=('GET', 'POST')) 
@login_required
def trip(tid):
    cur1 = g.conn.execute("SELECT * FROM countries ORDER BY cname")
    cur2 = g.conn.execute(
        """SELECT DISTINCT c.country_id, c.cname FROM policies p, countries c 
        WHERE p.country_id = c.country_id ORDER BY c.cname;"""
    )
    return render_template("newtrip.html", cur1 = cur1, cur2 = cur2)


# add new itinerary
@app.route('/addtrip', methods=['POST'])
def addtrip():
    # gets traveler_id from session 
    traveler_id = session['tid']
    country_id_origin = request.form['country_id_origin']
    country_id_destination = request.form['country_id_destination']
    travel_date = request.form['travel_date']
    departure_time = request.form['departure_time']
    # calls helper function to find correct policy for origin-destination pair
    policy_id = findPolicy(country_id_origin, country_id_destination)
    error = None

    if (not country_id_origin) or (not country_id_destination):
       error = "Please provide an origin and destiniation country" 
    elif not travel_date:
        error = "Please include a travel date for your trip"  
    elif not policy_id:
        error = "Could not locate located a covid-19 travel policy for this trip"
    elif not traveler_id: 
        error = "Traveler id could not be found"    
    if checkTravelDate(travel_date) == False:
        error = "Travel date cannot be in the past"
    # if traveler does not enter time, its set to null since it's not required
    if not departure_time:
        departure_time = None

    # SQL for inserting the intinerary
    if error is None:
        try:
            g.conn.execute(
                """INSERT INTO itineraries(country_id_origin, country_id_destination, 
                policy_id, traveler_id, travel_date, departure_time) 
                VALUES (%s,%s,%s,%s,%s,%s)""", (country_id_origin, country_id_destination, 
                policy_id, traveler_id, travel_date, departure_time)
            )
            # get recently-added trip policy
            pName = ''
            pURL = ''
            cur = g.conn.execute(
                "SELECT * FROM policies WHERE policy_id = '{}'".format(policy_id)
            )
            if cur.rowcount > 0 and cur.rowcount < 2:
                for r in cur: 
                    pName = r['pname']
                    pUrl = r['policy_data']
                cur.close()
                # policy link 
                pLink = '{}'.format(pUrl)
                # gets recently added itinerary 
                cur2 = g.conn.execute(
                    """SELECT * FROM Itineraries WHERE traveler_id = '{}' AND travel_date = '{}'
                    AND country_id_origin = '{}' AND country_id_destination = '{}'
                    """.format(session['tid'], travel_date, country_id_origin, 
                    country_id_destination)
                )
                # gets traveler's name
                cur3 = g.conn.execute(
                    """SELECT t.fname, t.lname FROM travelers t where t.traveler_id = '{}'
                    """.format(session['tid'])
                )
                # gets countries for new trip dropdowns on policy page
                # origin query 
                cur4 = g.conn.execute("SELECT * FROM countries ORDER BY cname")
                # destination query
                cur5 = g.conn.execute(
                            """SELECT DISTINCT c.country_id, c.cname 
                            FROM policies p, countries c 
                            WHERE p.country_id = c.country_id 
                            ORDER BY c.cname"""
                        )   
                return render_template("policy.html", 
                        cur2=cur2, cur3 = cur3, pLink = pLink, pName = pName,
                        cur4 = cur4, cur5 = cur5
                )
            else:
                error = "Could not create a new trip"
        # pass on IntegrityError so our error message shows
        except IntegrityError as e:
            pass

    # asks traveler to try again if not successful 
    flash(error)
    return redirect(url_for('trip', tid = session['tid']))

# helper method for finding policy for an origin-destination pair
def findPolicy(origin, dest):
    # creates a list of the riskgroup ids for each policy that a destination-country uses
    destRiskGroups = []
    error = None 
    cur = g.conn.execute(
        "SELECT * FROM policies WHERE country_id = '{}'".format(dest)
    )
    for r in cur: 
        destRiskGroups.append(r['group_id']) 
    cur.close
    if len(destRiskGroups) != 0:
        # uses a helper method to find out which riskgroup the origin falls into
        group_id = getGroup(destRiskGroups, origin)

    # if it gets a riskgroup id, we can now select the correct policy and return the policy id
        if group_id != null:
            cur2 = g.conn.execute(
                """SELECT policy_id FROM policies WHERE country_id = '{}' 
                AND group_id = '{}'""".format(dest, group_id)
            )
            for r in cur2: 
                pid = r['policy_id']
            cur2.close()
            return pid
    # this error message never gets flashed, but it helps w/ understanding what happened...
    else: 
        error = "Could not locate located a covid-19 travel policy for this trip"

# helper method for finding correct risk group for an origin-dest pair 
# takes a list of destination's policies' riskgroups, and finds out which 
# one applies to the origin country 
def getGroup(destRiskGroups, origin):
    for riskGroup in destRiskGroups:       
        cur = g.conn.execute(
            """SELECT group_id FROM Member_Of WHERE country_id = '{}' 
            AND group_id = '{}'""".format(origin, riskGroup)
        )
    if cur.rowcount >= 0: 
        return riskGroup

#helper method for making sure travel date is not in the past
def checkTravelDate(travelDate):
    from datetime import date
    from datetime import datetime
    
    todayDate = date.today()
    travelDate = datetime.strptime(travelDate, '%Y-%m-%d')
    travelDate = datetime.date(travelDate)
    if travelDate >= todayDate:
        return True
    else:
        return False


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
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(debug=debug, threaded=threaded, host=host, port=port)

    run()




