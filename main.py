import requests
import sys

api_key = "0DowkZk6qFmZnOJNxCbySSjS7qHLOJE6rJwxERfY1pwS25bifGjZa9x7Ax5EVlqc"
url = "https://www.thebluealliance.com/api/v3"
headers = {
    "X-TBA-Auth-Key": api_key
}
event_key = "2025oncmp1"

teamsJson = requests.get(f"{url}/event/{event_key}/teams", headers=headers).json()
teamsJson.sort(key=lambda team: team["team_number"])

progress = 0

def generateText():
    global progress
    finalText = ""
    numTeams = len(teamsJson)

    for team in teamsJson:
        teamMatches = requests.get(f"{url}/team/{team["key"]}/event/{event_key}/matches", headers=headers).json()
        teamMatches.sort(key=lambda match: match["match_number"])

        finalText += f"# {team["team_number"]}: {team["nickname"]}\n"

        for match in teamMatches:
            finalText += f"- Q{match["match_number"]}\n"

        progress += 1
        print(f"{round(progress/numTeams * 100)}%", end="\r")

    print(finalText)

generateText()