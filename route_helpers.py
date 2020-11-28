BASE_URL = 'https://api.covidtracking.com/v1/'

def find_state_data(state):
    """call the COVID tracking API for current data"""
    f"{BASE_URL}/states/{state}/current.json"