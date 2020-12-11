import requests
from datetime import datetime


BASE_URL = 'https://api.covidtracking.com/v1/'


us_states_dict = {
    "al": "Alabama",
    "ak": "Alaska",
    "as": "American Samoa",
    "az": "Arizona",
    "ar": "Arkansas",
    "ca": "California",
    "co": "Colorado",
    "ct": "Connecticut",
    "de": "Delaware",
    "dc": "District Of Columbia",
    "fm": "Federated States Of Micronesia",
    "fl": "Florida",
    "ga": "Georgia",
    "gu": "Guam",
    "hi": "Hawaii",
    "id": "Idaho",
    "il": "Illinois",
    "in": "Indiana",
    "ia": "Iowa",
    "ks": "Kansas",
    "ky": "Kentucky",
    "la": "Louisiana",
    "me": "Maine",
    "mh": "Marshall Islands",
    "md": "Maryland",
    "ma": "Massachusetts",
    "mi": "Michigan",
    "mn": "Minnesota",
    "ms": "Mississippi",
    "mo": "Missouri",
    "mt": "Montana",
    "ne": "Nebraska",
    "nv": "Nevada",
    "nh": "New Hampshire",
    "nj": "New Jersey",
    "nm": "New Mexico",
    "ny": "New York",
    "nc": "North Carolina",
    "nd": "North Dakota",
    "mp": "Northern Mariana Islands",
    "oh": "Ohio",
    "ok": "Oklahoma",
    "or": "Oregon",
    "pw": "Palau",
    "pa": "Pennsylvania",
    "pr": "Puerto Rico",
    "ri": "Rhode Island",
    "sc": "South Carolina",
    "sd": "South Dakota",
    "tn": "Tennessee",
    "tx": "Texas",
    "ut": "Utah",
    "vt": "Vermont",
    "vi": "Virgin Islands",
    "va": "Virginia",
    "wa": "Washington",
    "wv": "West Virginia",
    "wi": "Wisconsin",
    "wy": "Wyoming"
	}

def add_commas(state_data, keys):
    """Add's commas to number from API"""
    for key in keys:
        state_data[f"{key}"] = "{:,}".format(int((state_data[f"{key}"])))
    return state_data


def get_state_data(state):
    """call the COVID tracking API for current data of individual state"""
    
    resp = requests.get(f"{BASE_URL}/states/{state}/current.json")

    if resp.status_code != 200:
        flash('The COVID Tracker API is experiencing an error, please come back later', 'danger')
        send_myself_err_email("get_state_data status code NOT 200")
    
    state_data = resp.json()

    # API only provides abbreviation of state - adding state name for UI
    state_data['full_st_name'] = us_states_dict[state]

    # # adding commas to #'s from API
    # state_data['positiveIncrease'] = "{:,}".format(state_data['positiveIncrease'])
    # state_data['totalTestResultsIncrease'] = "{:,}".format(state_data['totalTestResultsIncrease'])
    # state_data['positive'] = "{:,}".format(state_data['positive'])
    # state_data['hospitalizedCurrently'] = "{:,}".format(state_data['hospitalizedCurrently'])
    # state_data['hospitalizedIncrease'] = "{:,}".format(state_data['hospitalizedIncrease'])
    # state_data['inIcuCurrently'] = "{:,}".format(state_data['inIcuCurrently'])
    # state_data['onVentilatorCurrently'] = "{:,}".format(state_data['onVentilatorCurrently'])

    state_data = add_commas(state_data, ['positiveIncrease', 'totalTestResultsIncrease', 'positive', 'hospitalizedCurrently', 'inIcuCurrently', 'onVentilatorCurrently', 'deathIncrease', 'death', 'recovered'])

    return state_data

def get_multi_state_data(user_favorites):
    
    multi_states_data = []
    for fav in user_favorites:
        resp = requests.get(f"{BASE_URL}/states/{fav}/current.json")
        state_data = resp.json()
        multi_states_data.append(state_data)

# adding ability to change abr to full name
        # for state in multi_states_data:
        #     state['full_st_name'] = us_states_dict[state]           

    return multi_states_data

def get_formatted_date(date):
    """Changing API date format to format for UI"""
    try:
        date = str(date)
        new_date = date[0] + date[1] + date[2] + date[3] + "-" + date[4] + date[5] + "-" + date[6] + date[7]
        d = datetime.strptime(str(new_date), "%Y-%m-%d")
        d = d.date()
        date_for_UI = d.isoformat()
    except (ValueError, IndexError):
        date_for_UI = "date not availble"
        send_myself_err_email("get_formatted_date Error - check API endpoints")
    return date_for_UI
