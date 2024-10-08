import requests, re

# Take in Email ID from user
id = input("Enter an email ID: ")

# Construct URL
url = "https://www.ecs.soton.ac.uk/people/" + id

# Fetch respinse from web page
response = requests.get(url)

# Use Regular Expression to pull name out of the returned HTML
names = re.findall('"name": ".*"', response.text)

if len(names) != 0: # if regex search worked, otherwise the email ID didn't yield a match
    name = names[1][9:-1] # strip out excess characters
    print(name)
else:
    print("Unable to find person by email ID")

# HTTP error feedback
if response.status_code == 404:
    print("An error occured reaching the web page")
elif response.status_code != 200:
    print("Unexpected response. Code:", response.status_code)
