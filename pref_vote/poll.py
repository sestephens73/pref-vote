class Vote:
    def __init__(self, candidate, rank):
        self.candidate = candidate # A string with the candidate's name (not a candidate class)
        self.rank = rank           # The rank of the candidate for this vote

class Ballot:
    def __init__(self, votes, id):
        self.votes = votes  # A list of "vote" objects
        self.id = id        # Integer, don't pass in 0

class Poll:
    def __init__(self, ballots, id):
        self.ballots = ballots  # A list of "Ballot" objects
        self.id = id
