import requests

def fetch_map_data():
    url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    
    if response.status_code == 200:
        map_data = response.text.strip().split('\n')
        map_array = [list(map(int, row.split())) for row in map_data]
        return map_array
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    map_array = fetch_map_data()
    if map_array:
        for row in map_array:
            print(row)