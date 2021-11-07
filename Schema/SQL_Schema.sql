CREATE TABLE Countries(
    country_id varchar(2),
    cname varchar(200) NOT NULL, --NOT NULL?
    PRIMARY KEY (country_id)
    -- Cannot map participation constraint with Risk Groups
)

CREATE TABLE Risk_Groups(
    group_id varchar(20), --Change to Serial
    gname varchar(30) NOT NULL,
    PRIMARY KEY (group_id)
)

CREATE TABLE Travelers(
    traveler_id Serial, --Change to Serial
    fname varchar(30) NOT NULL, 
    lname varchar(30) NOT NULL,
    vax_status boolean NOT NULL, 
    citizenship varchar(2) NOT NULL, 
    dob date CHECK (dob < CURRENT_TIMESTAMP) NOT NULL, 
    PRIMARY KEY (traveler_id),
    FOREIGN KEY (citizenship) REFERENCES Countries
    -- Cannot map participation constraint with Countries
)

CREATE TABLE Itineraries(
    itinerary_id Serial, --Change to Serial
    travel_date date CHECK (travel_date >= CURRENT_TIMESTAMP) NOT NULL,
    departure_time time, 
    traveler_id Serial NOT NULL, --Change to Serial
    policy_id varchar (20) NOT NULL, --lookups for creating itinerary-policy -- relationship will go thru Flies_To relationship...change value to serial
    country_id_origin varchar(2) NOT NULL, 
    country_id_destination varchar(2) NOT NULL, 
    PRIMARY KEY (itinerary_id),
    FOREIGN KEY (traveler_id) REFERENCES Travelers,
    FOREIGN KEY (policy_id) REFERENCES Policies, 
    FOREIGN KEY (country_id_origin, country_id_destination) REFERENCES Flies_To (country_id_origin, country_id_destination) 
    -- Cannot map participation constraint with Countries, Policies, and Travelers
)

-- origin risk group mapping
CREATE TABLE Member_Of(
    country_id varchar(2), --origin country id
    group_id varchar(20), --risk groups origin falls into...change to serial
    PRIMARY KEY (country_id, group_id),
    FOREIGN KEY (country_id) REFERENCES Countries,
    FOREIGN KEY (group_id) REFERENCES Risk_Groups
)

CREATE TABLE Policies(
    policy_id varchar(20), --Change to Serial
    pname varchar(30) NOT NULL,
    valid_from date,
    valid_to date, 
    vax_policy boolean, 
    policy_data varchar(500) NOT NULL,
    country_id varchar(2) NOT NULL, --destination (policy holder)
    group_id varchar(20) NOT NULL, --risk group (origin risk groups)..change to serial
    PRIMARY KEY (policy_id),
    FOREIGN KEY (country_id) REFERENCES Countries, 
    FOREIGN KEY (group_id) REFERENCES Risk_Groups
    -- Cannot map participation constraints with Risk Groups and Countries
)

CREATE TABLE Flies_To(
    country_id_origin varchar(2), 
    country_id_destination varchar(2), 
    PRIMARY KEY (country_id_origin, country_id_destination),
    FOREIGN KEY (country_id_origin) REFERENCES Countries,
    FOREIGN KEY (country_id_destination) REFERENCES Countries
)






