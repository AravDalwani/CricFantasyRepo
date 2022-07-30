import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/44156/overs"

headers = {
	"X-RapidAPI-Key": "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743",
	"X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}


responsetest_ = requests.request("GET", url, headers=headers)

information_match = responsetest_.json()

print(information_match['overs'])

print(information_match['batTeam']['teamScore'])
print(information_match['batTeam']['teamWkts'])