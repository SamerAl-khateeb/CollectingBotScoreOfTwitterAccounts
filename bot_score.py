# bot_score.py                       By: Samer Al-khateeb
# a script that reads a CSV file contain twitter usernames
# and output each username and it's bot score as returned 
# from the Botometer API. The score will be in range [0-1]
# representing the probability of an account being a bot. 
# Am account with a score close to 1 is mostlikely a bot account, 
# while an account with a score close to 0 is mostlikely a human 
# account. We multiply the returned score by 100 to get a score 
# from [0-100] instead of [0-1].

# Dependencies: you might need to install the following libraries 
# before you can run this code.
# For Mac users, open terminal and type:
#       python3 -m pip install botometer
#       python3 -m pip install tweepy
# For Windows users, open CMD and type:
#       py -m pip install botometer
#       py -m pip install tweepy

#importing necessary modules for Botometer Library 
import botometer
import tweepy
import time
import json
import requests
import csv


def write_output_to_CSV(biglist):
        columnNames = ["UserName", "BotScore"]
        filename = "botScoresOutput.csv"
        # creating a file to save the output
        with open(filename, 'w', newline='', encoding='utf-8') as csvOutputFile:
                # creating a csv writer object
                csvwriter = csv.writer(csvOutputFile, delimiter=',', lineterminator='\n')
                #write the columns headers
                csvwriter.writerow(columnNames)
                csvwriter.writerows(biglist)


def main():
        ############### insert your APPs credentials below #################
        rapidapiKey = "PasteYourRapidKeyAPIHere!"
        twitterAppAuth = {
                'consumer_key': 'PasteYourConsumerKeyHere!',
                'consumer_secret': 'PasteYourConsumerSecretHere!',
                'access_token': 'PasteYourAccessTokenHere!',
                'access_token_secret': 'PasteYourAccessTokenSecretHere!',
        }
        ########################################################################
        bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapiKey,
                          **twitterAppAuth)
        
        # counter to keep track of how many accounts we processed
        count = 0
        
        #creating a list to hold the output values so we can write it to CSV file
        CSVOutputList =[]
        
        #variable that hold the file name
        inputFilename = 'input.csv'

        #open the input file and read it
        with open(inputFilename, newline='', encoding='utf-8') as csvInputFile:
                CSVFileAsList = csv.reader(csvInputFile, skipinitialspace=True)
                
                # skipping the first row in the csv input file
                next(CSVFileAsList)
                # for each row in the CSV file send the account to the API
                for row in CSVFileAsList:
                        UserName = row[0]
                        print()
                        count += 1
                        try:
                                check_score = bom.check_account("@" + UserName)
                                print("we are processing user number : " + str(count) + "\t with screen name @" + UserName)
                                bot_score = check_score['raw_scores']['universal']['overall']
                                print(UserName," " , bot_score*100)
                                # multiply the returned score by 100
                                bot_score = bot_score * 100

                        # Tweepy Rate Limit Error Check
                        except tweepy.error.RateLimitError:
                                print("exceeded rate limit, sleeping for 15 minutes")
                                time.sleep(60*15)

                        # Tweepy Crawling Error
                        except tweepy.TweepError as te:
                                error = str(te)
                                print("Actual count : " + str(count) + "\t skipping " + UserName + " because: " + error)
                                print("gave it a score of -1")
                                bot_score = -1

                        # No Timeline Found
                        except botometer.NoTimelineError as bte:
                                error = str(bte)
                                print("Actual count : " + str(count) + "\t skipping " + UserName + " because: " + error)
                                print("gave it a score of -1")
                                bot_score = -1

                        # HTTP Error 500 Handling
                        except requests.exceptions.HTTPError as reqhttpE:
                                error = str(reqhttpE)
                                print("Actual count : " + str(count) + "\t skipping " + UserName + " because: " + error)
                                print("gave it a score of -1")
                                bot_score = -1
                        
                        # If the username is incorrectly formatted
                        except TypeError:
                                print("TypeError for user " + str(UserName))
                                print("gave it a score of -1")
                                bot_score = -1

                        #creating a list of values (a row) 
                        CSVOutputRow = [UserName, bot_score]

                        #adding the row to the list of output
                        CSVOutputList.append(CSVOutputRow)
                        
                        # if you processed 500 accounts you 
                        # reached the maximum number of requests 
                        # allowed for the basic plan. So Sleep 
                        # for 24 hours then continue
                        if (count == 500):
                                time.sleep(86400)
                                print("Sleeping for 24 hours!")
                                count = 0

                # when you finish processing all the account 
                # write the result to a csv file
                write_output_to_CSV(CSVOutputList)


if __name__ == "__main__":
    main()
