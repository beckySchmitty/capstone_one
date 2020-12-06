import requests
from datetime import datetime


BASE_URL = 'https://api.covidtracking.com/v1/'


us_states_dict = {
	'al':'Alabama',
	'ak': 'Alaska',
	'az': 'Arizona',
	'Arkansas': 'AR',
	'ca':'California',
	'Colorado': 'CO',
	'Connecticut': 'CT',
	'Delaware': 'DE',
	'District ofColumbia': 'DC',
	'Florida': 'FL',
	'Georgia': 'GA',
	'Hawaii': 'HI',
	'Idaho': 'ID',
	'Illinois': 'IL',
	'Indiana': 'IN',
	'Iowa': 'IA',
	'Kansas': 'KS',
	'Kentucky': 'KY',
	'Louisiana': 'LA',
	'Maine': 'ME',
	'Maryland': 'MD',
	'Massachusetts': 'MA',
	'Michigan': 'MI',
	'Minnesota': 'MN',
	'Mississippi': 'MS',
	'Missouri': 'MO',
	'Montana': 'MT',
	'Nebraska': 'NE',
	'Nevada': 'NV',
	'New Hampshire': 'NH',
	'New Jersey': 'NJ',
	'New Mexico': 'NM',
	'ny':'New York',
	'North Carolina': 'NC',
	'North Dakota': 'ND',
	'oh': 'Ohio',
	'Oklahoma': 'OK',
	'Oregon': 'OR',
	'Pennsylvania': 'PA',
	'Rhode Island': 'RI',
	'South Carolina': 'SC',
	'South Dakota': 'SD',
	'Tennessee': 'TN',
	'Texas': 'TX',
	'Utah': 'UT',
	'Vermont': 'VT',
	'Virginia': 'VA',
	'Washington': 'WA',
	'West Virginia': 'WV',
	'Wisconsin': 'WI',
	'Wyoming': 'WY',
    'American Samoa': 'as',
    'Guam': 'gu',
    'Northern Mariana Islands': 'mp',
    'U.S. Virgin Islands': 'vi'
}

def get_state_data(state):
    """call the COVID tracking API for current data of individual state"""
    
    resp = requests.get(f"{BASE_URL}/states/{state}/current.json")

    if resp.status_code != 200:
        flash('The COVID Tracker API is experiencing an error, please come back later', 'danger')
        send_myself_err_email("get_state_data status code NOT 200")
    
    state_data = resp.json()

    # API only provides abbreviation of state - adding state name for UI
    state_data['full_st_name'] = us_states_dict[state]

    return state_data

def get_multi_state_data(user_favorites):
    
    multi_states_data = []
    for fav in user_favorites:
        resp = requests.get(f"{BASE_URL}/states/{fav}/current.json")
        state_data = resp.json()
        multi_states_data.append(state_data)

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
