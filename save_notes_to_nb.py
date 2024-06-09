import requests, json, subprocess, re

URL = "http://192.168.0.112:5000/notes"

def get_notes():
	response = requests.get(URL, params={"the_p": "@3rooycA -1"})
	return response.json()

try:
	notes = get_notes()["notes"]
except:
	exit()

if not notes:
	exit()

for note in notes:
	content = note["content"]
	idd = note["id"]
	is_todo = note["is_todo"]
	is_bookmark = note["is_bookmark"]
	timestamp = note["timestamp"]
	tags = note["tags"]

	if tags:
		tags = ",".join(tags)
		#remove # from tags
		tags = tags.replace("#", "")

	print(tags)

	# check if content is a url
	match = re.search(r"(?P<url>https?://[^\s]+)", content)
	if is_bookmark and match and not is_todo:
		if tags:
			subprocess.run(["nb", match[0], "--tags", tags])
		else:
			subprocess.run(["nb", match[0]])
		continue

	if is_todo:
		if tags:
			subprocess.run(["nb", "todo", "a", "--description", content, "--tags", tags])
		else:
			subprocess.run(["nb", "todo", "a", "--description", content])
	else:
		if tags:
			subprocess.run(["nb", "a", "--description", content, "--tags", tags])
		else:
			subprocess.run(["nb", "a", "--description", content])

	para = {"the_p": "@3rooycA -1", "id": str(idd)}
	response = requests.delete(URL, params=para)
	print("="*50)

