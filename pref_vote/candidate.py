class Candidate:
    def __init__(self, name):
        self.name = name # A string with the name of the candidate
        self.total_votes = 0 # The candidate's running total of votes
        self.has_won = False # Boolean determining whether the candidate has won yet
        self.is_eliminated = False # Boolean determining whether the candidate has been eliminated
