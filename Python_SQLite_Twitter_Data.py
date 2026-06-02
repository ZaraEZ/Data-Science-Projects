'''
Zara Zarzour
DSC 450

We are going to work with a small extract of tweets (about 200 of them), available here:  http://dbgroup.cdm.depaul.edu/DSC450/Module5.txt 

a.	Create a SQL table to contain the following attributes of a tweet:
"created_at", "id_str", "text", "source", "in_reply_to_user_id", “in_reply_to_screen_name”, “in_reply_to_status_id”, 
"retweet_count", “contributors”. Please assign reasonable data types to each attribute and use SQLite for this assignment.
	
b.	Write python code to read through the Module5.txt file and populate your table from part a.  
Make sure your python code reads through the file and loads the data properly (including NULLs).

'''
import sqlite3
import json
from asyncio.windows_events import NULL


conn = sqlite3.connect('dsc450.db') # open the connection
cursor = conn.cursor()

file = open('C:/Users/zara/OneDrive/Desktop/DePaul/DSC450-Databases/Assignment-5/submission/Module5.txt', 'r', encoding='utf-8') #open file in read mode

data = file.readline().split("EndOfTweet")

#string that holds the SQLite command to create a table
createtbl1 = """
CREATE TABLE Tweets
(
    created_at VARCHAR2(38),
    id_str VARCHAR2(38),
    text VARCHAR(140),
    source VARCHAR(60),
    in_reply_to_user_id VARCHAR2(38),
    in_reply_to_screen_name VARCHAR2(38),
    in_reply_to_status_id NUMBER(20),
    retweet_count NUMBER(10),
    contributors VARCHAR2(38),
    
    CONSTRAINT TweetsPK
        PRIMARY KEY (id_str) 
);
"""

cursor.execute("DROP TABLE IF EXISTS Tweets;")  # drop the table, if existing

cursor.execute(createtbl1) # create table

tweets = []
for i in data:
    tweets.append(json.loads(i)) #append all tweet data to list

#Here I converted all NULL strings to an actual NULL within the list since I was having issues with NULL not showing up right 
tweets_formatted = []
for i in tweets:
    if i == 'NULL':
        tweets_formatted.append(NULL)
    else:
        tweets_formatted.append(i)
            
for feature in tweets_formatted: # feature is the data
    created_at = feature["created_at"]
    id_str = feature["id_str"]
    txt = feature["text"]
    sourc_e = feature["source"]
    reply_user_id = feature["in_reply_to_user_id"]
    reply_screen_name = feature["in_reply_to_screen_name"]
    reply_status_id = feature["in_reply_to_status_id"]
    retweet_count = feature["retweet_count"]
    contributors = feature["contributors"]

    #insert into sqlite table
    cursor.execute("INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [created_at, id_str, txt, sourc_e, reply_user_id, reply_screen_name, reply_status_id, retweet_count, contributors]) 

#Display one row only
cursor.execute("SELECT * FROM Tweets")
rows = cursor.fetchone()
for row in rows:
    print(row)

#display all rows 
'''cursor.execute("SELECT * FROM Tweets")
for row in cursor:
    print(str(row).strip(",)").strip("("))'''
    
conn.commit()
conn.close()