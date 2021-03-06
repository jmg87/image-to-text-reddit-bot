#!/usr/bin/python
import os
import sys
import praw
#from StringIO import StringIO
from google.cloud import vision
from google.cloud.vision import types

# Define PRAW parameters

reddit = praw.Reddit('bot1') # bot1 defined in file praw.ini in located in the same folder

# Ask on which subreddit we are going to work:

subredditToScan = input("Which subreddit would you like to scan?: ")
with open("human_transcribed.txt","r") as r:
    human_transcribed = r.read()
    human_transcribed = human_transcribed.split("\n")
    human_transcribed = list(filter(None,human_transcribed))
    if subredditToScan not in human_transcribed:
        subreddit = reddit.subreddit(subredditToScan)
    else:
        print("This subreddit already has human transcribers and don't like bots to take their jobs")

#Function to call the Cloud Vision API and fetch it the target urls

def scan_images(url):
    client  = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = url
    response = client.text_detection(image=image)
    text = response.text_annotations
    print(text[0].description)
    return text[0].description

#Function to format the text to post it as a code block on reddit

def format_text(rawtext):
    formatted_text = ""
    for line in rawtext.split("\n"):
        formatted_text += "    " + line + "\n  "
    return formatted_text

#Function to post the formatted text to reddit

def post_comment(ocr_data):
    submission.reply(ocr_data + "\n\n __________________________________________ \n\n Beta bot on its way to becoming Skynet. Please direct all hate and complaints to my master /u/audscias , thank you.  ^^More ^^info ^^r/image_to_text_beta")


#Function to detect the context of the image
"""
def context(url):
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = url
    response = client.label_detection(image=image)
    labels = response.label_annotations
    for label in labels:
        print(label.description)
"""







#Find the top 10 hot submissions on the subreddit and check wether we already scanned them or not

for submission in subreddit.hot(limit=10):
    if not os.path.isfile("posts_replied_to.txt"): #Create the replied to list file if it doesn't exist
        with open("posts_replied_to.txt","a"):
            if submission.domain == "i.redd.it" :
                text = scan_images(submission.url)
                #labels = context(submission.url)
                formatted_text = format_text(text)
                post_comment(formatted_text)
                with open("posts_replied_to.txt","w") as f:
                    posts_replied_to = list(filter(None, posts_replied_to))
                    posts_replied_to.append(submission.id)
                    for post_id in posts_replied_to:
                        f.write(post_id + "\n")

    else:
        with open("posts_replied_to.txt","r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None,posts_replied_to))
            if submission.domain == "i.redd.it" and submission.id not in posts_replied_to:
                text = scan_images(submission.url)
                #labels = context(submission.url)
                formatted_text = format_text(text)
                post_comment(formatted_text)
                with open("posts_replied_to.txt","w") as f:
                    posts_replied_to = list(filter(None, posts_replied_to))
                    posts_replied_to.append(submission.id)
                    for post_id in posts_replied_to:
                        f.write(post_id + "\n")
