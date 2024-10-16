import requests
from bs4 import BeautifulSoup

def get_locations_in_glasgow(file_path=None):
    url = "https://geographic.org/streetview/scotland/glasgow_city/glasgow.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    location_list = soup.find("ul")
    for location in location_list.find_all("li"):
        location_name = location.find("a").text
        location_string = location.text

        results.append(location_name)

    if file_path is not None:
        open(file_path, "w").write("\n".join(results))
    return results

if __name__ == '__main__':
    results = get_locations_in_glasgow("../data/locations.txt")
    # print(results)