import requests


BASE_URL = 'https://api.covidtracking.com/v1/'

def get_state_data(state):
    """call the COVID tracking API for current data"""
    resp = requests.get(f"{BASE_URL}/states/{state}/current.json")

    state_data = resp.json()

    return state_data