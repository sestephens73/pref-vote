from math import floor
from poll import Vote, Ballot, Poll, Candidate

def run_STV_poll(poll): # Pass in a poll
    threshold = floor(len(poll.ballots)/(poll.num_winners + 1) + 1)
    winners = {}
    remaining_eligible_candidates = len(poll.candidates)
    for b in poll.ballots:
        if 1 in b.votes:
            b.votes[1]
            if b.votes[1].candidate in poll.candidates:
                poll.candidates[b.votes[1].candidate].total_votes += 1
            b.votes[1].counted = True
    while len(winners) < poll.num_winners and remaining_eligible_candidates > poll.num_winners - len(winners):
        top_eligible_candidate = poll.candidates[max([candidate for candidate in poll.candidates.values() if candidate.is_eligible], key=Candidate.total_votes)]
        if top_eligible_candidate.total_votes >= threshold:
            top_eligible_candidate.has_won = True
            top_eligible_candidate.is_eligible = False
            winners[len(winners) + 1] = top_eligible_candidate.name
            remaining_eligible_candidates -= 1
            redistribute_winner_votes(top_eligible_candidate, poll)
        else:
            bot_eligible_candidate = poll.candidates[min([candidate for candidate in poll.candidates.values() if candidate.is_eligible], key=Candidate.total_votes)]
            bot_eligible_candidate.is_eligible = False
            remaining_eligible_candidates -= 1
            redistribute_loser_votes(bot_eligible_candidate, poll)
    return winners

def redistribute_winner_votes(cand, poll)
    pass

def redistribute_loser_votes(cand, poll)
    for b in poll.ballots:
        last_vote_rank = max({vote.rank: vote for vote in b.votes if vote.counted == True}, key=Vote.rank)
    return
