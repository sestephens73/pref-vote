class Vote: # Represents a single candidate paired with a preference rank
    def __init__(self, candidate, rank):
        self.candidate = candidate # A string with the candidate's name (not a candidate class)
        self.rank = rank           # The rank of the candidate for this vote
        self.counted = False       # Tells whether this vote has been counted yet

class Ballot: # One person's full ballot with all their ranked candidates
    def __init__(self, votes, id):
        self.votes = {vote.rank: vote for vote in votes}  # A list of "vote" objects
        self.id = id

class Candidate: # One candidate
    def __init__(self, name):
        self.name = name # A string with the name of the candidate
        self.total_votes = 0 # The candidate's running total of votes
        self.has_won = False # Boolean determining whether the candidate has won yet
        self.is_eligible = True # Boolean determining whether the candidate is still eligible. Set to false if candidate wins or is eliminated from the bottom of the running.

class Poll: # A full poll whose winners need to be determined
    def __init__(self, poll_name, candidates, id, num_winners):
        self.name = poll_name
        self.candidates = {candidate.name: candidate for candidate in candidates} # Pass in a list of "Candidate" objects. Makes a dictionary, key is string of candidate names, value is corresponding candidate object.
        self.ballots = []  # A list of "Ballot" objects
        self.id = id            # The poll id
        self.num_winners = num_winners # The number of winners for the given poll

    def print_all_candidate_info(self):
        for c in self.candidates.values():
            print(c.name, c.total_votes, c.has_won, c.is_eligible)

    def submit_ballot(self, ballot):
        self.ballots.append(ballot)
