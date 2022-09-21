# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []

    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = ""
        try:
            description = translate_html(entry.description)
        except:
            description = translate_html(entry.title_detail)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        #newsStory = NewsStory(guid, title, description, link, pubdate)
        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
# TODO: NewsStory
class NewsStory(object):
    #stories_list = []
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower() # case-insensitive

    def is_phrase_in(self, text):
        phrase = str(self.phrase) # string
        words_phrase = phrase.split() # split phrase into words

        text = str.lower(text) # case-insensitive and string
        words_text = '' #changing text from 0 -> adding
        for c in text: # iterate through text
            if c in string.punctuation:
                #text.replace(c, ' ')
                words_text = words_text + ' ' # add whitespace
            else:
                words_text = words_text + c # add good letters
        words_text = words_text.split() # split into words by whitespace
# row of 3 white spaces -> word contain empty space "" -> delete/remove
        while "" in words_text:
            words_text.remove("")
        for word in words_phrase:
            if word in words_text and phrase in ' '.join(words_text):
                found = True
            else:
                return False
        return found

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    #def __init__(self, phrase): not necessary
    #    PhraseTrigger.__init__(self, phrase) not necessary
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    #def __init__(self, phrase): not necessary
    #    PhraseTrigger.__init__(self, phrase) not necessary
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        time = str(time) # double check -> string
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S") # time
        #time = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %z")
        time = time.replace(tzinfo=pytz.timezone("EST")) # timezone
        self.time = time

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        #story.get_pubdate() = datetime.strptime(get_pubdate(), "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.time


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return (self.trigger1.evaluate(story) or self.trigger2.evaluate(story))# or (self.trigger1.evaluate(story) and self.trigger2.evaluate(story))
        # either one (OR BOTH)
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    triggered_stories = [] # make a list of triggered_stories
    for story in stories: # iterate through all the stories
       for trigger in triggerlist: # list with triggers conditions, e.g. t1, t4
            if trigger.evaluate(story): # trigger is met within the story
                triggered_stories.append(story) # add to the triggered_stories = []
    return triggered_stories # stories -> necessary to change -> no sense of giving back all the stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    trigger_dictionary = {} # store trigger names as keys such as a, Trump
    trigger_list = []

    #for line in range(len(lines)):
    for line in lines:
        #elements = lines[line].split(",") # split each lines by , into elements
        elements = line.split(",")
        if elements[1] == "TITLE": # element 1 in txt file
            trigger_dictionary[elements[0]] = TitleTrigger(elements[2])
            # store "election" in the trigger_dictionary
        elif elements[1] == "DESCRIPTION":
            trigger_dictionary[elements[0]] = DescriptionTrigger(elements[2])
        elif elements[1] == "AFTER":
            trigger_dictionary[elements[0]] = AfterTrigger(elements[2])
        elif elements[1] == "BEFORE":
            trigger_dictionary[elements[0]] = BeforeTrigger(elements[2])
        elif elements[1] == "NOT":
            trigger_dictionary[elements[0]] = NotTrigger(elements[2])
        elif elements[1] == "AND":
            trigger_dictionary[elements[0]] = AndTrigger(elements[2], elements[3])
        elif elements[1] == "OR":
            trigger_dictionary[elements[0]] = OrTrigger(elements[2], elements[3])
        elif elements[0] == "ADD":
            for behind_add in range(1, len(elements)): # iterate from 1 (because of ADD)
            # to the end of line
                trigger_list.append(trigger_dictionary[elements[behind_add]])
    return trigger_list

    print(lines) # for now, print it so you see what it contains!


SLEEPTIME = 120 #seconds -- how often we poll


if __name__ == '__main__':
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("a")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Reads and writes Newsstories to stories.txt in specified format
        # Retrieves and filters the stories from the RSS feeds
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                guidShown.append(newstory.get_guid())

        while True:


            print("Polling . . .", end=' ')
            # Get stories from BBC's Top Stories RSS news feed
            stories = process("http://feeds.bbci.co.uk/news/rss.xml")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))


            stories = filter_stories(stories, triggerlist)


            #@ISMAMA
            file = open('stories.txt', 'w')
            for s in stories:
                file.write(s.title.strip())
                file.write("\n")
                for i in range(len(s.title)):
                    file.write("-")
                file.write("\n")
                file.write(s.description.strip())
                file.write("\n")
                file.write(s.link.strip())
                file.write("\n")
                file.write("_"*60)
                for s in range(2):
                    file.write("\n")
            file.close()

            #Do not uncomment these lines
            #Dlist(map(get_cont, stories))
            #Dscrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)