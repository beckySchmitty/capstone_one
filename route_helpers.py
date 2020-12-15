import requests
from datetime import datetime

BASE_URL = 'https://api.covidtracking.com/v1/'

#***************************************************************************************** API HELPERS
def get_state_data(state):
    """call the COVID tracking API for current data of individual state"""
    
    resp = requests.get(f"{BASE_URL}/states/{state}/current.json")

    if resp.status_code != 200:
        flash('The COVID Tracker API is experiencing an error, please come back later', 'danger')
    
    state_data = resp.json()

    # Update data to fit UI needs
    state_data = format_for_UI(state_data, state, ["positiveIncrease", "totalTestResultsIncrease", "positive", "hospitalizedCurrently", "inIcuCurrently", "onVentilatorCurrently", "deathIncrease", "death", "recovered", "negative", "pending"], "homestate")

    return state_data

def get_multi_state_data(user_favorites):
    
    multi_states_data = []
    for address in user_favorites:
        resp = requests.get(f"{BASE_URL}/states/{address.state_name}/current.json")
        state_data = resp.json()

        # Update data to fit UI needs
        state_data = format_for_UI(state_data, address.state_name, ["positiveIncrease", "hospitalizedCurrently", "death"], address.nickname)

        multi_states_data.append(state_data)
         
    return multi_states_data

def get_us_deaths():
    resp = requests.get(f"{BASE_URL}/us/daily.json")

    if resp.status_code != 200:
        flash('The COVID Tracker API is experiencing an error, please come back later', 'danger')

    entire_us_data = resp.json()

    entire_us_data[0]["death"] = "{:,}".format((entire_us_data[0]["death"]))
    us_deaths = entire_us_data[0]["death"]

    return us_deaths


#***************************************************************************************** UI HELPERS

def format_for_UI(data, state, keys_lst, nickname):
        data['full_st_name'] = us_states_dict[state]
        data['date'] = get_formatted_date(data['date'])
        data = add_commas(data, keys_lst)
        data['nickname'] = nickname

        return data


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
    return date_for_UI

def add_commas(state_data, keys):
    """Add's commas to number from API"""
    for key in keys:
        if state_data[f"{key}"] is not None:
            state_data[f"{key}"] = "{:,}".format(int((state_data[f"{key}"])))
        else:
            state_data[f"{key}"] = "-"
    return state_data

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
