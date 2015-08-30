'''
Brent Read
8/30/2015
bread@princeton.edu

Reads in the given CSV file and returns a list of subscription IDs, 
subscription tupe, and the duration of the subscription
'''

import csv
from datetime import datetime
import time
#Reads in the CSV file and returns a dictionary
#The dictionary is a string key followed by a list of lists, where each inner list is a set of transaction identifiers
def process_CSV(fileName):
	userList = {}
	with open(fileName, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			subscription_ID = row[1]
			row.pop(1) #Remove the item from the list
			#If we already have seen this user, add a new entry
			if subscription_ID in userList:
				#Add onto the current list to preserve history
				currentList = userList[subscription_ID]
				currentList.append(row)
				userList[subscription_ID] = currentList
			#This is the first time we've seen this subscription ID, so we make a new list
			else:
				listOfLists = []
				listOfLists.append(row)
				#userList looks like [[row]]
				userList[subscription_ID] = listOfLists
	return userList

#Takes a string key, ID, and a dictionary of users, userList
#Returns a string of the number of days between the first and last subscrption
#If the user only has one subscription, the last subscription is taken as the current date
def get_subscription_duration(userList, ID):
	transactionList  = userList[ID]
	firstTransaction = transactionList[0][2]
	lastTransaction  = transactionList[-1][2]

	if get_subscription_type(userList, ID) == "One-off":
		lastTransaction = time.strftime("%m/%d/%Y")
	firstDate = datetime.strptime(firstTransaction, "%m/%d/%Y")
	lastDate  = datetime.strptime(lastTransaction, "%m/%d/%Y")

	return str(abs((lastDate - firstDate).days)) + " days"

#Takes a string key, ID, and a dictionary of users, userList
#Returns a string of the type of subscription for a given key, ID
def get_subscription_type(userList, ID):
	transactionList  = userList[ID]
	if len(transactionList) is 1:
		return "One-off"
	firstTransaction = transactionList[0][2]
	lastTransaction  = transactionList[1][2]

	firstDate = datetime.strptime(firstTransaction, "%m/%d/%Y")
	lastDate  = datetime.strptime(lastTransaction, "%m/%d/%Y")


	delta = int((lastDate - firstDate).days)

	if delta > 300:
		return "Yearly"
	if delta > 27:
		return "Monthly"
	return "Daily" 

#Main defines the name of the CSV file and returns list of users followed by the subscription type and duration
def main():
	fileName = 'subscription_report.csv'
	userDict = process_CSV(fileName)
	for key in userDict:
		if key != "Subscription ID":
			finalResult = []
			finalResult.append(key)
			finalResult.append(get_subscription_type(userDict, key))
			finalResult.append(get_subscription_duration(userDict, key))  
			print finalResult

if __name__ == "__main__":
	main()