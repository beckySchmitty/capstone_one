import requests
from datetime import datetime


BASE_URL = 'https://api.covidtracking.com/v1/'

def get_state_data(state):
    """call the COVID tracking API for current data"""
    resp = requests.get(f"{BASE_URL}/states/{state}/current.json")

    state_data = resp.json()

    return state_data

def get_multi_state_data(user_favorites):

    multi_states_data = []
    for fav in user_favorites:
        resp = requests.get(f"{BASE_URL}/states/{fav}/current.json")
        state_data = resp.json()
        multi_states_data.append(state_data)

    return multi_states_data

def get_formatted_date(date):
    try:
        date = str(date)
        new_date = date[0] + date[1] + date[2] + date[3] + "-" + date[4] + date[5] + "-" + date[6] + date[7]
        d = datetime.strptime(str(new_date), "%Y-%m-%d")
        d = d.date()
        date_for_UI = d.isoformat()
    except (ValueError, IndexError):
        date_for_UI = "date not availble"
    return date_for_UI

def send_myself_err_email(error):

    msg = Message("ERROR: Capstone Project",
                  sender="beckySchmittyDev@gmail.com",
                  recipients=["becky.schmitthenner@gmail.com"])

    msg.body = f"{error}"
    msg.html = f"{error}"

    mail.send(msg)