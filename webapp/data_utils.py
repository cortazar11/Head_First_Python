import DBcm
import platform

#db_details = "CoachDB.sqlite3"
if "aws" in platform.uname().release:
    db_details = {
        "host": "cortazar11.mysql.pythonanywhere-services.com",
        "user": "cortazar11",
        "password": "Eskoriatza1*",
        "database": "cortazar11$default",
    
        }
else:
        db_details = {
        "host": "localhost", 
        "user": "root", 
        "password": "Eskoriatza1*", 
        "database": "swimDB",
    }

from queries import *


def get_swim_sessions():
    """Return a tuple-list of unique session timestamps."""
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SESSIONS)
        results = db.fetchall()
    return results


def get_session_swimmers(date):
    """When given a date (YYYY-MM-DD), return a tuple-list of swimmers
    and their associated age (filtered by date).
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_BY_SESSION, (date,))
        results = db.fetchall()
    return results


def get_swimmers_events(name, age, date):
    """When given a date (YYYY-DD-MM), swimmer's name, and swimmer's age, return
    a tuple-list of events the swimmer swam on that date."""
    with DBcm.UseDatabase(db_details) as db:
        db.execute(
            SQL_SWIMMERS_EVENTS_BY_SESSION,
            (
                name,
                age,
                date,
            ),
        )
        results = db.fetchall()
    return results


def get_swimmers_times(name, age, distance, stroke, date):
    """When given a date (YYYY-MM-DD), swimmer's name, swimmer's age, distance, and stroke,
    return a tuple-list of times the swimmer swam on that date over the identified
    distance/stroke combination."""
    with DBcm.UseDatabase(db_details) as db:
        db.execute(
            SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
            (
                name,
                age,
                distance,
                stroke,
                date,
            ),
        )
        results = db.fetchall()
    return results