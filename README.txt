TwitterBot

This bot was written inspired by an article I read regarding winning Twitter contests using automation.
Contests with the form of "RT to win" or "RT and follow to win" etc are scanned and added to a queue for processing.
One the queue is piled up, one by one is checks for a follow request and a like request and addresses those accordingly.

Features:
BotSpotter - Bot spotting accounts were troublesome so I developed a line or two of code to make sure I did not follow bots
or anything that appeared to be a bot. It also maintains a black lit of these users.

Unfollow Bot - To avoid hitting my hard limit of 5000 follows, every 3 weeks users will be unfollowed.