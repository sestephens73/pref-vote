class Vote:
    def __init__(self, candidate, rank):
        self.candidate = candidate # A string with the candidate's name (not a candidate class)
        self.rank = rank           # The rank of the candidate for this vote
        self.counted = False       # Tells whether this vote has been counted yet

class Ballot:
    def __init__(self, votes, id):
        self.votes = {vote.candidate: vote for vote in votes}  # A list of "vote" objects
        self.id = id        # Integer, don't pass in 0

class Candidate:
    def __init__(self, name):
        self.name = name # A string with the name of the candidate
        self.total_votes = 0 # The candidate's running total of votes
        self.has_won = False # Boolean determining whether the candidate has won yet
        self.is_eliminated = False # Boolean determining whether the candidate has been eliminated


class Poll:
    def __init__(self, candidates, ballots, id, num_winners):
        self.candidates = {candidate.name: candidate for candidate in candidates} # Pass in a list of "Candidate" objects
        self.ballots = ballots  # A list of "Ballot" objects
        self.id = id            # The poll id
        self.num_winners = num_winners # The number of winners for the given poll
