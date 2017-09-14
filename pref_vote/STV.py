from math import floor
from poll import *

def run_STV_poll(poll): # Pass in a poll
    threshold = floor(len(poll.ballots)/(poll.num_winners + 1) + 1)
    for b in poll.ballots:
        if 1 in b.votes:
            b.votes[1]
            if b.votes[1].name in poll.candidates:
                poll.candidates[b.votes[1].candidate].total_votes += 1
            b.votes[1].counted = True
