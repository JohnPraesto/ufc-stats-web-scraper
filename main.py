from bs4 import BeautifulSoup
import requests
import pandas
import time

events_url = "http://www.ufcstats.com/statistics/events/completed?page="
page_number = 1
response_events_page = requests.get(events_url + str(page_number))
events_soup = BeautifulSoup(response_events_page.text, "html.parser")
all_events_on_this_page = events_soup.find_all("tr")
all_fights_list = []

for event in all_events_on_this_page[4:]:
    event_info = event.find("a", class_="b-link b-link_style_black")
    print(f"Entering {event_info.text.strip()}")
    time.sleep(1)
    fights_url = event_info["href"]
    date = event.find("span", class_="b-statistics__date")
    location = event.find("td", class_="b-statistics__table-col b-statistics__table-col_style_big-top-padding")

    response_fights_page = requests.get(fights_url)

    fights_soup = BeautifulSoup(response_fights_page.text, "html.parser")

    # This is a list of all fights in the event shown in table rows, each row has info about one fight
    all_fights_of_this_event = fights_soup.find_all("tr")

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
            "fighter_2": fighter[1].text.strip(),   # Second fighter name
            "date": date.text.strip(),
            "location": location.text.strip()
            }

            all_fights_list.append(fight_details)

all_fights_df = pandas.DataFrame(all_fights_list)

print(all_fights_df)
all_fights_df.to_csv("all_ufc_fights.csv", index=False)



# TODO do so that it does all pages of events