from bs4 import BeautifulSoup
import requests
import pandas
import time

# url = "http://www.ufcstats.com/event-details/ad23903ef3af7406"
# url = "http://www.ufcstats.com/event-details/4956f60b7fa57c1a"
url = "http://www.ufcstats.com/event-details/6a8a06b542e1516d"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

all_fights_list = []

# This is a list of all fights in the event shown in table rows, each row has info about one fight
all_fights_of_this_event = soup.find_all("tr")

# For each fight of the event
for fight in all_fights_of_this_event:
    
    # This class contains the word "win", "draw", or "NC".
    outcome = fight.find("i", class_="b-flag__text")

    # In the forst table row if the page all table data are empty.
    # So if outcome is not empty
    if outcome:

        # This class contains the names of the fighters
        fighter = fight.find_all("a", class_="b-link b-link_style_black")

        fight_details = {
        "outcome": outcome.text.strip(),
        "fighter_1": fighter[0].text.strip(),  # First fighter name
        "fighter_2": fighter[1].text.strip()   # Second fighter name
        }

        all_fights_list.append(fight_details)

all_fights_df = pandas.DataFrame(all_fights_list)

print(all_fights_df)