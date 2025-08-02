"""
FTC Points Calculator
This script calculates advancement points for FTC teams based on the 2025-2026 Advancement point changes.

Author: Alberto
Organization: FTC Team 772
Date: 2024-10-01
Version: 1.0.0

This script fetches data from the FIRST API, processes it to calculate advancement points for teams, and exports the results to JSON and CSV files.
It uses the requests library to interact with the API, pandas for data manipulation, and pathlib for file handling.

"""

# Imports
from FIRSTAPIKey import API_USER, API_PASS
import requests
import pandas as pd
from sys import argv
from requests.auth import HTTPBasicAuth
from pathlib import Path

#API Login Info
auth = HTTPBasicAuth(API_USER, API_PASS)

# Event Info (Pass in through command line arguments) nevermind, hardcoded for now.
EVENT_ID = "ROCMP"
EVENT_YEAR = "2024"

#URLS
url_dict = {
    "awards" : "http://ftc-api.firstinspires.org/v2.0/" + str(EVENT_YEAR) + "/awards/" + str(EVENT_ID),
    "teams" : "http://ftc-api.firstinspires.org/v2.0/" + str(EVENT_YEAR) + "/rankings/" + str(EVENT_ID),
    "alliance" : "http://ftc-api.firstinspires.org/v2.0/" + str(EVENT_YEAR) + "/alliances/" + str(EVENT_ID),
    "matches" : "http://ftc-api.firstinspires.org/v2.0/" + str(EVENT_YEAR) + "/matches/" + str(EVENT_ID)
}

#JSON Responses
response_dict = {
    "awards" : requests.get(url_dict["awards"], auth=auth),
    "teams" : requests.get(url_dict["teams"], auth=auth),
    "alliance" : requests.get(url_dict["alliance"], auth=auth),
    "matches" : requests.get(url_dict["matches"], auth=auth, params={"tournamentLevel": "playoff"})
}

#Dataframes based on responses.
df_dict = {
    "awards" : pd.DataFrame(data=response_dict["awards"].json()["awards"]),
    "team_rank" : pd.DataFrame(data=response_dict["teams"].json()["rankings"]),
    "alliance" : pd.DataFrame(data=response_dict["alliance"].json()["alliances"]),
    "matches" : pd.DataFrame(data=response_dict["matches"].json()["matches"])
}

#Index Setting
df_dict["awards"].set_index(keys="teamNumber", inplace=True)
df_dict["team_rank"].set_index(keys="teamNumber", inplace=True)
df_dict["alliance"].set_index(keys="number", inplace=True)
df_dict["matches"].set_index(keys="series", inplace=True)

# Sort the matches DataFrame by series in descending order
# This ensures that the most recent matches are at the top.
df_dict["matches"].sort_index(ascending=False, inplace=True)

# Remove Dean's List Awards Winners and Tournament Finalists/Winners from the awards DataFrame
df_dict["awards"] = df_dict["awards"][~df_dict["awards"]["awardId"].isin([19, 10, 12, 13])]
# Remove nAn teams from the awards DataFrame
df_dict["awards"] = df_dict["awards"][~df_dict["awards"].index.isna()]
# Convert the index of the awards DataFrame to integer type
df_dict["awards"].index = df_dict["awards"].index.astype(int)

#print(df_dict["awards"].head())

# Create a DataFrame for Advancement Points
# This DataFrame will hold the points for each team based on their achievements.
df_advancement_points = pd.DataFrame(index=df_dict["team_rank"].index.values, columns=["totalPoints", "qualPoints", "alliancePoints", "playoffPoints", "awardPoints"])

# Set number of teams
num_teams = len(df_dict["team_rank"].index.values)

# Calculate Advancement Points based on Qualifier Rank for each team
for idx, row in df_dict["team_rank"].iterrows():

    qual_rank_points = 0
    alliance_rank_points = 0
    playoff_points = 0
    award_points = 0

    rank = row["rank"]

    # Step 1: Calculate points for each team based on their qualifier rank.
    # Normalize the rank to a point value between 2 and 16 (Min-Max Normalization)
    qual_rank_points = int(16 - (rank - 2) * (16 - 2) / (max(df_dict["team_rank"]["rank"]) - min(df_dict["team_rank"]["rank"])))

    # Step 2: Calculate points based on the team's alliance (If applicable).
    if idx in df_dict["alliance"]["captain"].values or idx in df_dict["alliance"]["round1"].values:
        try:
            # If the team is a captain, substract their alliance number from 21 to get points.
            alliance_rank_points = 21 - df_dict["alliance"].index[df_dict["alliance"].captain == idx][0]
        except KeyError:
            # If the team is a pick, substract their alliance number from 21 to get points.
            alliance_rank_points = 21 - df_dict["alliance"].index[df_dict["alliance"].round1 == idx][0]
        except IndexError:
            alliance_rank_points = 21 - df_dict["alliance"].index[df_dict["alliance"].round1 == idx][0]


    # Step 3: Calculate points based on the team's playoff performance (if applicable).
    # ONLY look at last 3-4 matches in the playoff series.

    # If the team was in the last 4 matches of the playoff series, consider them for playoff points.
    # Get the last 4 matches of the playoff series
    last_matches = df_dict["matches"].head(4)

    match_count = 0

    # Check if the team was part of any of these matches
    if any(idx in [team["teamNumber"] for team in match["teams"]] for _, match in last_matches.iterrows()):
        # If the team was in the first match, but was not dqed, they get 40 points. (Tournament Winner)
        for i in range(4):
            if last_matches.iloc[match_count]["teams"][i]["teamNumber"] == idx:

                match_winner = "bwoah"

                if last_matches.iloc[match_count]["scoreRedFinal"] > last_matches.iloc[0]["scoreBlueFinal"]:
                    match_winner = "Red"
                else:
                    match_winner = "Blue"
                
                # If the team was on the winning alliance, they get 40 points (Winner).
                if match_winner in last_matches.iloc[match_count]["teams"][i]["station"]: #DQed IS FALSE EVERY TIME!!!
                    playoff_points = 40
                    break
                # If the team was on the losing alliance, they get 20 points (Runner Up).
                else:
                    playoff_points = 20
                    break
        
        match_count += 1

        #Check if the second match contains the same team as the first match.
        # If so, that means that there was a tiebreaker match.
        # Skip this mathch and continue to the next one to avoid miscounting.
        if last_matches.iloc[match_count]["teams"][0]["teamNumber"] == last_matches.iloc[match_count-1]["teams"][0]["teamNumber"] and last_matches.iloc[match_count]["teams"][match_count]["teamNumber"] == last_matches.iloc[match_count-1]["teams"][0]["teamNumber"] and last_matches.iloc[match_count]["teams"][2]["teamNumber"] == last_matches.iloc[match_count-1]["teams"][0]["teamNumber"] and last_matches.iloc[match_count]["teams"][3]["teamNumber"] == idx:
            match_count += 1

        # If the team was in the second match, but was dqued, they get 10 points. (Third Place)
        for i in range(4):
            if last_matches.iloc[match_count]["teams"][i]["teamNumber"] == idx:

                if last_matches.iloc[match_count]["scoreRedFinal"] > last_matches.iloc[0]["scoreBlueFinal"]:
                    match_winner = "Red"
                else:
                    match_winner = "Blue"

                if match_winner not in last_matches.iloc[match_count]["teams"][i]["station"]:
                    playoff_points = 10
                    break

        match_count += 1

        
        # If the team was in the third match, but was dqed, they get 5 points. (Fourth Place)
        for i in range(4):

            if last_matches.iloc[match_count]["scoreRedFinal"] > last_matches.iloc[0]["scoreBlueFinal"]:
                match_winner = "Red"
            else:
                match_winner = "Blue"

            if last_matches.iloc[match_count]["teams"][i]["teamNumber"] == idx and match_winner not in last_matches.iloc[0]["teams"][i]["station"]:
                playoff_points = 5

    # Step 4: Calculate points based on the team's awards (if applicable).

    awards_rows = pd.DataFrame(df_dict["awards"].loc[[idx]]) if idx in df_dict["awards"].index else pd.DataFrame()

    award_points = 0

    if not awards_rows.empty:
        # Check for Inspire Award (ID 11) and its series
        inspire_rows = awards_rows[awards_rows["awardId"] == 11]
        if not inspire_rows.empty:
            if (inspire_rows["series"] == 1).any():
                award_points = 60
            elif (inspire_rows["series"] == 2).any():
                award_points = 30
            elif (inspire_rows["series"] == 3).any():
                award_points = 15
        # Check for other awards
        else:
            if (awards_rows["series"] == 1).any():
                award_points += 12
            if (awards_rows["series"] == 2).any():
                award_points += 6
            if (awards_rows["series"] == 3).any():
                award_points += 3
    else:
        award_points = 0


    # Step 5: Calculate total points for the team.
    total_points = qual_rank_points + alliance_rank_points + playoff_points + award_points

    #print(total_points)

    # Step 6: Update the DataFrame with the total points for the team.
    df_advancement_points.loc[idx, "totalPoints"] = total_points
    df_advancement_points.loc[idx, "qualPoints"] = qual_rank_points
    df_advancement_points.loc[idx, "alliancePoints"] = alliance_rank_points
    df_advancement_points.loc[idx, "playoffPoints"] = playoff_points
    df_advancement_points.loc[idx, "awardPoints"] = award_points

# Sort the DataFrame by points in descending order
df_advancement_points.sort_values(by="totalPoints", ascending=False, inplace=True)

# Print the DataFrame with team numbers and their advancement points
print(df_advancement_points.head(10))

# Export the DataFrame to a JSON file

output_path = Path(f"C:/VSCProjects/FTC Points Calculator/export")

df_advancement_points.to_json(output_path / "JSON" / f"advancement_points_{EVENT_ID}_{EVENT_YEAR}.json", index=True)
df_advancement_points.to_csv(output_path / "CSV" / f"advancement_points_{EVENT_ID}_{EVENT_YEAR}.csv")



