import requests

# mining of https://intro.nyc/councilmembers

import requests
import csv
from bs4 import BeautifulSoup


PUBLIC_ADVOCATE_NAME = "Public Advocate Jumaane Williams"
ENACTED = "status-enacted"
NEEDS_SIGNATURE = "status-enacted-mayor-s-desk-for-signature-"
IN_COMMITTEE = "status-committee"
LAID_OVER_IN_COMMITTEE = "status-laid-over-in-committee"
WITHDRAWN = "status-withdrawn"


URL = "https://intro.nyc/councilmembers"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

members = soup.find_all("span", class_="full-name")
links = [member.find("a").get("href") for member in members]
members = [member.find("a").text for member in members]


public_advocate_index = members.index(PUBLIC_ADVOCATE_NAME)
members.pop(public_advocate_index)
links.pop(public_advocate_index)


districts = soup.find_all("span", class_="district")
districts = [d.text for d in districts]

parties = soup.find_all("span", class_="party")
parties = [p.text for p in parties]
parties.pop(public_advocate_index)

boroughs = soup.find_all("span", class_="borough")
boroughs = [b.text for b in boroughs]

committees = soup.find_all("td", class_="committees")
committees.pop(public_advocate_index)


data = []

for member, link, district, party, borough in zip(
    members, links, districts, parties, boroughs
):

    URL = f"https://intro.nyc/{link}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    enacted = []
    needs_signature = []
    in_committee = []
    laid_over = []
    withdrawn = []

    legislation = soup.find_all("div", class_="legislation")
    for l in legislation:
        if "Introduced" not in l.find("span", class_="attribution").text:
            status = l["class"][-1]

            if status == ENACTED:
                enacted.append(l)
            elif status == NEEDS_SIGNATURE:
                needs_signature.append(l)
            elif status == IN_COMMITTEE:
                in_committee.append(l)
            elif status == LAID_OVER_IN_COMMITTEE:
                laid_over.append(l)
            elif status == WITHDRAWN:
                withdrawn.append(l)
            else:
                print(f"Unclear status {status}")

    print(member)
    datum = [
        member,
        link,
        district,
        party,
        borough,
        len(enacted),
        len(needs_signature),
        len(in_committee),
        len(laid_over),
        len(withdrawn),
    ]
    data.append(datum)


header = [
    "name",
    "link",
    "district",
    "party",
    "borough",
    "num_enacted",
    "num_needs_signature",
    "num_in_committee",
    "num_laid_over",
    "num_withdrawn",
]

with open("2022-legislators.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)
