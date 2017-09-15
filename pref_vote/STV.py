from math import floor
from poll import Vote, Ballot, Candidate, Poll

# Takes a Poll object, and returns a dictionary keyed with placings with values of lists of winning candidates
def run_STV_poll(poll): # Pass in a Poll object
    threshold = floor(len(poll.ballots)/(poll.num_winners + 1) + 1) # Droop quota

    """
    winners: A dictionary of all winners, to be returned.
    Key is an integer, the place.
    Value is a list (in case of ties) of strings, the winning candidates
    """
    winners = {}
    total_winners = 0 # Definite winners that have been found at a given time
    remaining_eligible_candidates = len(poll.candidates)

    for b in poll.ballots: # Loop through all the ballots and tally up the first choices
        if 1 in b.votes:
            if b.votes[1].candidate in poll.candidates:
                poll.candidates[b.votes[1].candidate].total_votes += 1
            b.votes[1].counted = True

    while total_winners < poll.num_winners:
        if remaining_eligible_candidates <= poll.num_winners - total_winners: # This ends the poll.
            while len([candidate for candidate in poll.candidates.values() if candidate.is_eligible]) > 0:
                highest_num_of_votes = max([candidate for candidate in poll.candidates.values() if candidate.is_eligible], key=lambda x:x.total_votes).total_votes
                top_eligible_candidates = [candidate for candidate in poll.candidates.values() if candidate.is_eligible and candidate.total_votes == highest_num_of_votes]
                if len(top_eligible_candidates) > 1:
                    top_eligible_candidates = break_winner_tie(top_eligible_candidates, poll)
                for c in top_eligible_candidates:
                    c.has_won = True
                    c.is_eligible = False
                    remaining_eligible_candidates -= 1
                    if total_winners + 1 not in winners:
                        winners[total_winners + 1] = []
                    winners[total_winners + 1].append(c.name)
                for c in top_eligible_candidates:
                    total_winners += 1
            return winners
        highest_num_of_votes = max([candidate for candidate in poll.candidates.values() if candidate.is_eligible], key=lambda x:x.total_votes).total_votes
        top_eligible_candidates = [candidate for candidate in poll.candidates.values() if candidate.is_eligible and candidate.total_votes == highest_num_of_votes]
        if len(top_eligible_candidates) > 1:
            top_eligible_candidates = break_winner_tie(top_eligible_candidates, poll)
        if highest_num_of_votes >= threshold: # Takes care of when there's a winner in this "voting round"
            for c in top_eligible_candidates:
                c.has_won = True
                c.is_eligible = False
                remaining_eligible_candidates -= 1
                if total_winners + 1 not in winners:
                    winners[total_winners + 1] = []
                winners[total_winners + 1].append(c.name)
            for c in top_eligible_candidates:
                total_winners += 1
                if c.total_votes > threshold:
                    redistribute_votes(c, True, poll, threshold)
        else: # Takes care of when the round has no winner, so the bottom candidate(s) are eliminated
            lowest_num_of_votes = min([candidate for candidate in poll.candidates.values() if candidate.is_eligible], key=lambda x:x.total_votes).total_votes
            bot_eligible_candidates = [candidate for candidate in poll.candidates.values() if candidate.is_eligible and candidate.total_votes == lowest_num_of_votes]
            if len(bot_eligible_candidates) > 1:
                bot_eligible_candidates = break_loser_tie(bot_eligible_candidates, poll)
            if len(bot_eligible_candidates) == remaining_eligible_candidates: # This means the poll is complete. There will be extra winners due to ties (extremely unlikely).
                for c in bot_eligible_candidates:
                    c.has_won = True
                    c.is_eligible = False
                    if total_winners + 1 not in winners:
                        winners[total_winners + 1] = []
                    winners[total_winners + 1].append(c.name)
                    return winners
            for c in bot_eligible_candidates:
                c.is_eligible = False
                remaining_eligible_candidates -= 1
            for c in bot_eligible_candidates:
                redistribute_votes(c, False, poll, threshold)
    return winners

# Redistributs the votes of a candidate who is no longer eligible. Redistributes all of a bottom candidate's votes. Redistributes surplus of a winning candidate's votes, fractionally.
def redistribute_votes(cand, is_for_winner, poll, threshold):
    for b in poll.ballots:
        prev_vote_rank = max({vote.rank: vote for vote in b.votes.values() if vote.counted == True}, key=lambda x:x)
        cur_vote_rank = prev_vote_rank + 1
        if b.votes[prev_vote_rank].candidate == cand.name:
            done = False
            while done == False and cur_vote_rank in b.votes:
                    cur_vote = b.votes[cur_vote_rank]
                    if poll.candidates[cur_vote.candidate].is_eligible:
                        increment = 1;
                        if is_for_winner:
                            increment = (cand.total_votes - threshold) / cand.total_votes
                        poll.candidates[cur_vote.candidate].total_votes += increment
                        done = True
                    cur_vote.counted = True
                    cur_vote_rank += 1
    return

# Function that breaks the ties of a number of winners
def break_winner_tie(tied_cands, poll):
    n = 1           # Which rank of tied votes the candidates are on
    while len(tied_cands) > 1:
        most_votes = 0 # Running highest votes for this layer (rank)
        winning_cands = []
        for c in tied_cands: # For each candidate
            cur_cand_votes = 0
            # Tally up all the nth place votes for the current candidate across all ballots
            for b in poll.ballots: # For each ballot
                if n in b.votes and b.votes[n].candidate == c.name: # If that vote layer exists and the vote is for the current candidate
                    cur_cand_votes += 1
            # If new winner, set most_votes
            if cur_cand_votes > most_votes:
                most_votes = cur_cand_votes
                winning_cands = [c]
            # If tied with rest of candidates, just add current one to the list for next tiebreaker
            elif cur_cand_votes == most_votes:
                winning_cands.append(c)
        # Set up for next loop.
        tied_cands = winning_cands
        if n > len(poll.candidates): # In case there's a perfect tie and all votes have been taken into account
            return tied_cands
        n += 1
    return tied_cands

# Function that breaks the ties of a number of losers
def break_loser_tie(tied_cands, poll):
    n = 1           # Which rank of tied votes the candidates are on
    while len(tied_cands) > 1:
        fewest_votes = len(poll.ballots) + 1 # Running lowest votes for this layer (rank)
        losing_cands = []
        for c in tied_cands: # For each candidate
            cur_cand_votes = 0
            # Tally up all the nth place votes for the current candidate across all ballots
            for b in poll.ballots: # For each ballot
                if n in b.votes and b.votes[n].candidate == c.name: # If that vote layer exists and the vote is for the current candidate
                    cur_cand_votes += 1
            # If new loser, set fewest_votes
            if cur_cand_votes < fewest_votes:
                fewest_votes = cur_cand_votes
                losing_cands = [c]
            # If tied with rest of candidates, just add current one to the list for next tiebreaker
            elif cur_cand_votes == fewest_votes:
                losing_cands.append(c)
        # Set up for next loop.
        tied_cands = losing_cands
        if n > len(poll.candidates): # In case there's a perfect tie and all votes have been taken into account
            return tied_cands
        n += 1
    return tied_cands
