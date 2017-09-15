from pref_vote.poll import Vote, Ballot, Poll, Candidate
from pref_vote.STV import run_STV_poll

def test_Vote():
    uut = Vote("Sean", 2)
    assert(uut.candidate == "Sean")
    assert(uut.rank == 2)
    assert (uut.counted == False)

def test_Ballot():
    test_Votes = [Vote("Sean", 1), Vote("Neil", 2)]
    uut = Ballot(test_Votes, 1234)
    assert(uut.votes[1] == test_Votes[0])
    assert(uut.votes[2] == test_Votes[1])

def test_Candidate():
    uut = Candidate("Neil")
    assert(uut.name == "Neil")
    assert(uut.total_votes == 0)
    assert(uut.has_won == False)
    assert(uut.is_eligible == True)

def test_Poll():
    test_Votes_1 = [Vote("Sean", 1), Vote("Neil", 2)]
    test_Votes_2 = [Vote("John", 2), Vote("Cob", 1)]
    test_Ballots = [Ballot(test_Votes_1, 1234), Ballot(test_Votes_2, 5678)]
    test_Candidates = [Candidate("Sean"), Candidate("Neil"), Candidate("John"), Candidate("Cob")]
    uut = Poll(test_Candidates, test_Ballots, 9012, 1)

    assert(uut.candidates["Sean"] == test_Candidates[0])
    assert(uut.candidates["Neil"] == test_Candidates[1])
    assert(uut.candidates["John"] == test_Candidates[2])
    assert(uut.candidates["Cob"] == test_Candidates[3])

    assert(uut.ballots == test_Ballots)
    assert(uut.id == 9012)
    assert(uut.num_winners == 1)

def test_simple_poll_1():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 1)

    assert(run_STV_poll(test_Poll) == {1:"A"})

def test_simple_poll_2():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 2)

    assert(run_STV_poll(test_Poll) == {1:"A", 2:"B"})

def test_simple_poll_3():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:"A", 2:"B", 3:"C"})

def test_more_winners_than_candidates():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 4)

    assert(run_STV_poll(test_Poll) == {1:"A", 2:"B", 3:"C"})

def test_equal_number_winners_and_candidates():
    pass

def test_perfect_loser_tie():
    pass

def test_imperfect_loser_tie():
    pass

def test_perfect_winner_tie():
    pass

def test_imperfect_winner_tie():
    pass

def test_more_winners_than_allocated():
    pass

