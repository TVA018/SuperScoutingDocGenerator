import requests
import sys

print("Enter your API Key: ", end="")
api_key = input()
url = "https://www.thebluealliance.com/api/v3"
headers = {
    "X-TBA-Auth-Key": api_key
}
eventKey = "2025oncmp1"

progress = 0

def getData():
    global progress

    teamsJson = requests.get(f"{url}/event/{eventKey}/teams/simple", headers=headers).json()
    teamsJson.sort(key=lambda team: team["team_number"])

    finalText = ""
    numTeams = len(teamsJson)

    for team in teamsJson:
        teamKey = team["key"]
        teamNumber = team["team_number"]
        teamName = team["nickname"]

        teamMatches = requests.get(f"{url}/team/{teamKey}/event/{eventKey}/matches/simple", headers=headers).json()
        teamMatches.sort(key=lambda match: match["match_number"])

        finalText += f"{teamNumber}: {teamName}\n"

        for match in teamMatches:
            alliance = ""
            position = 0

            for allianceColor, allianceTeam in match["alliances"].items():
                if(teamKey in allianceTeam["team_keys"]):
                    position = allianceTeam["team_keys"].index(teamKey) + 1
                    alliance = allianceColor.title()
                    break

            finalText += f"- Q{match["match_number"]} ({alliance} {position})\n"

        progress += 1
        print(f"{round(progress/numTeams * 100)}%", end="\r")

    print(finalText)

getData()