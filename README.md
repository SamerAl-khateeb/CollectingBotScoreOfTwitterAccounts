# CollectingBotScoreOfTwitterAccounts
This repo contains a script that can be used to collect the Twitter account bot score using Botometer API.

## bot_scores.py
This script will read a CSV file with Twitter usernames and generate an output file containing the Twitter user bot score in a range of 1 to 100. This script uses the Botometer API to determine the likelihood of an account being a social bot. An account with a score close to 100 is most likely a bot, while an account with a score close to 0 is most likely a human. For the accounts that we could not retrieve their bot score (because they were set to private, were suspended by Twitter, or any other reason) we assigned them a score of -1.

## Input and Output
**input.csv** is a sample csv input file with two Twitter usernames.

**botScoresOutput.csv** is a sample csv output file with two Twitter usernames and their bot scores.