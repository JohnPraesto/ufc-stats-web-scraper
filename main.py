from bs4 import BeautifulSoup
import requests
import pandas
import time
from datetime import datetime

events_url = "http://www.ufcstats.com/statistics/events/completed?page="
page_number = 1
all_fights_list = []
todays_date = datetime.now()

while True:

    response_events_page = requests.get(events_url + str(page_number))
    events_soup = BeautifulSoup(response_events_page.text, "html.parser")
    all_events_on_this_page = events_soup.find_all("tr") # The tr tags contain info about and link to events

    print(events_url + str(page_number))
    print(f"length of all_events_on_this_page is {len(all_events_on_this_page)}")

    # When there is no events on the page there will only be two empty tr tags
    # Need better exit condition?
    if len(all_events_on_this_page) <= 2:
        print("program finished")
        break

    for event in all_events_on_this_page:

        date = event.find("span", class_="b-statistics__date")

        # The first couple of tr-tags does not contain event info.
        # And there is one tr-tag that is a future event.
        # This if/else-statement makes the for-loop skip invalid tr-tags
        if date:
            date_text = date.text.strip()
            date_object = datetime.strptime(date_text, "%B %d, %Y")
            if todays_date < date_object:
                print("date was from future")
                continue
        else:
            print("date was None")
            continue

        event_info = event.find("a", class_="b-link b-link_style_black")
        print(f"Entering {event_info.text.strip()}")

        time.sleep(1) # Delay not to overload the server

        fights_url = event_info["href"]
        location = event.find("td", class_="b-statistics__table-col b-statistics__table-col_style_big-top-padding")

        response_fights_page = requests.get(fights_url)

        fights_soup = BeautifulSoup(response_fights_page.text, "html.parser")

        # This is a list of all fights of the event (shown in table rows), each row has info about one fight
        all_fights_of_this_event = fights_soup.find_all("tr")

        # For each fight of the event
        for fight in all_fights_of_this_event:
            
            # This class contains the word "win", "draw", or "NC".
            outcome = fight.find("i", class_="b-flag__text")

            # The first tr-tag of this page does not contain fight info, so outcome will be None
            # This if-statement makes sure only valid tr-tags are handeled (they contain an outcome)
            if outcome:

                # This class contains the names of the fighters
                fighter = fight.find_all("a", class_="b-link b-link_style_black")

                fight_details = {
                "outcome": outcome.text.strip(),
                "fighter_1": fighter[0].text.strip(),
                "fighter_2": fighter[1].text.strip(),
                "date": date.text.strip(),
                "location": location.text.strip()
                }

                all_fights_list.append(fight_details)

    page_number += 1

all_fights_df = pandas.DataFrame(all_fights_list)
print(all_fights_df)
all_fights_df.to_csv("all_ufc_fights.csv", index=False)

# TODO Why is date and location within quotationmarks