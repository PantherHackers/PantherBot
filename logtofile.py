import datetime, os, io

def log(sc, response):
	#sets file location to the logs folder and based on the day's date
	#this way if $log is enabled and the day rolls over, it will shift over to the new file without hiccup
	filename = "logs/" + response["channel"] + " " + str(datetime.date.today()) + ".txt"

	#API call for user info that posted the message, personnally this should be removed
	#its innefficient (and causes unnecessary API calls), we should make a locally stored list of users that have talked and reference that
	#and if they arent found, call this function and append that list
	#TODO Use USER_LIST instead
	temp_user = sc.api_call(
		"users.info",
		user = response["user"]
	)

	script_dir = os.path.dirname(__file__)
	fullDir = os.path.join(script_dir, filename)
	#If the file isnt present already it makes a new one with the right name.
	if os.path.isfile(fullDir) == True:
		target = io.open(fullDir, "a", encoding='utf-8')
	else:
		target = io.open(fullDir, "w+",encoding='utf-8')
	user_name = temp_user["user"]["profile"]["first_name"] + " " + temp_user["user"]["profile"]["last_name"]

	#format:
	#F_NAME L_NAME
	#[MESSAGE] [TIMESTAMP]
	target.write(user_name+ "\n")
	target.write(response["text"] + " [")
	target.write(response["ts"] + "]\n\n")
	target.close()
