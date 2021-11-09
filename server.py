import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import psycopg2
from decouple import config #tool for hiding uri credentials 


app = Flask(__name__)   

# find a better way to do this...
# make sure to change later! 

uri = config('uri', default='')

# uri = "postgresql://andreasfreund:1234@localhost/dbproj1"
# uri = "postgresql://acf2175:6901@34.74.246.148/proj1part2"
engine = create_engine(uri)

# before request code from class
@app.before_request
def before_request():

    try: 
        g.conn = engine.connect()

    except:
        print("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None

# teardown code from class
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

# homepage that shows generic list of travelers
@app.route('/')
def index():

    print (request.args)

    cur = g.conn.execute("SELECT * From travelers")

    travelers = []

    for r in cur:
        travelers.append(r)

    cur.close()

    context = dict(data = travelers)

    return render_template("index.html", **context)


# page for addding a new trip 
@app.route('/trip')
def trip():

    print (request.args)

    return render_template("newtrip.html")


# add new traveler
@app.route('/add', methods=['POST'])
def add():

    fname = request.form['fname']
    lname = request.form['lname']
    vax_status = request.form['vax_status']
    citizenship = request.form['citizenship']
    dob = request.form['dob']
    # email = request.form['email']

    # add error handling

    g.conn.execute(
        "INSERT INTO travelers(fname, lname, vax_status, citizenship, dob) VALUES (%s,%s,%s,%s,%s)", (fname, lname, vax_status, citizenship, dob)
    )

    cur = g.conn.execute(
        "SELECT traveler_id FROM travelers WHERE fname = '{}' AND lname = '{}' AND vax_status = '{}' AND citizenship = '{}' AND dob = '{}' ".format(fname, lname, vax_status, citizenship, dob)
    )

    for r in cur:
        tid = r[0]

    # eventually redirect to add new trip with recently added traveler_id as url parameter...eventually we should use something unique like an email for this
    # return redirect('/addtrip/tid')
    return redirect('/')

# add new itinerary
@app.route('/addtrip/<tid>', methods=['POST'])
def addtrip(tid):
    country_id_origin = request.form['country_id_origin']
    country_id_destination = request.form['country_id_destination']
    travel_date = request.form['travel_date']
    departure_time = request.form['departure_time']
    # calls helper function to find correct policy for origin-destination pair
    policy_id = findPolicy(country_id_origin, country_id_destination)
    # !hardcoded! should be changed to a parameter passed in via the url 
    # traveler_id = 10
    traveler_id = tid

    # SQL for inserting the intinerary
    g.conn.execute(
        "INSERT INTO itineraries(country_id_origin, country_id_destination, policy_id, traveler_id, travel_date, departure_time) VALUES (%s,%s,%s,%s,%s,%s)", (country_id_origin, country_id_destination, policy_id, traveler_id, travel_date, departure_time)
    )

    # should redirect to policy page 
    return redirect('/')

# helper method for finding policy for an origin-destination pair
def findPolicy(origin, dest):
    # creates a list of the riskgroup ids for each policy that a destination   
    # country uses
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
            "SELECT policy_id FROM policies WHERE country_id = '{}' AND group_id = '{}' ".format(dest, group_id)
        )
    # not robust: doesn't check to make sure that cur2 only has 1 element...
    for r in cur2: 
        pid = r['policy_id'] 
    cur2.close()

    print(pid)
    return pid

# helper method for finding correct risk group for an origin-dest pair 
# takes a list of destination's policies' riskgroups, and finds out which 
# one applies to the origin country 
def getGroup(destRiskGroups, origin):

    if (len(destRiskGroups) != 0):
        for riskGroup in destRiskGroups:
            
            cur = g.conn.execute(
                "SELECT group_id FROM Member_of WHERE country_id = '{}' AND group_id = '{}'".format(origin, riskGroup)  
            )
        if cur.rowcount > 0:
            return riskGroup
            
# @app.route('/policies', methods=('GET', 'POST'))
# def policies():
#     cur = g.conn.execute("SELECT pname FROM policies")
#     names = []

#     for result in cur:
#         names.append(result['pname'])
#     cur.close()
#     return names

# adds variable to url which is the travelerID...we can use this for seeing a traveler's itineraries for instance

@app.route('/traveler/<tid>', methods=['GET', 'POST'])
def showTraveler(tid):
    cur = g.conn.execute("SELECT * FROM Travelers WHERE traveler_id='{}'".format(tid)) 

    fname = []

    for r in cur:
        fname.append(r["fname"])
    
    cur.close()
    context = dict(data = fname)
    return render_template("itineraries.html", **context)



# hello world page
@app.route('/hello')
def hello():
    return 'Hello, World!'


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