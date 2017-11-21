#!/usr/bin/python
import os
import re
import pdb
import sys
import wget
import praw
import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

# Function below not yet implemented. Next step.
def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))




reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("softwaregore")

for submission in subreddit.hot(limit=10):
    submissiondomain = submission.domain
    
    if  not os.path.isfile("posts_replied_to.txt"):
    	posts_replied_to = []
    else:
	with open("posts_replied_to.txt", "r") as f:
       		posts_replied_to = f.read()
       		posts_replied_to = posts_replied_to.split("\n")
    		posts_replied_to = list(filter(None, posts_replied_to))
		if submissiondomain == 'i.redd.it' and submission.id not in posts_replied_to:
        		print("Domain: ", submissiondomain)
        		print("Title", submission.title)
        		print("URL: ", submission.url)
			# image_data= _get_image(submission.url)
			# ocr_data= _get_image(image_data)
			ocr_data = process_image(submission.url)
			sys.stdout.write("The raw output from tesseract OCR for this image is:\n\n")
    			sys.stdout.write("-----------------BEGIN-----------------\n")
			sys.stdout.write(ocr_data)
			sys.stdout.write("\n")
    			sys.stdout.write("------------------END------------------\n")	 

			submission.reply(ocr_data + "\n\n __________________________________________ \n\n This is a bot in early beta. Please direct all hate and complaints to my master /u/audscias , thank you, puny humans\n ^^r/image_to_text_beta")
			posts_replied_to.append(submission.id)
			with open("posts_replied_to.txt", "w") as f:
    				for post_id in posts_replied_to:
	    				f.write(post_id + "\n")


 
