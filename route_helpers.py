import requests


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