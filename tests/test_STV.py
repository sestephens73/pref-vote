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
    uut = Poll('foo', test_Candidates, 9012, 1)
    for ballot in test_Ballots:
        uut.submit_ballot(ballot)

    assert(uut.candidates["Sean"] == test_Candidates[0])
    assert(uut.candidates["Neil"] == test_Candidates[1])
    assert(uut.candidates["John"] == test_Candidates[2])
    assert(uut.candidates["Cob"] == test_Candidates[3])

    assert(uut.ballots == test_Ballots)
    assert(uut.id == 9012)
    assert(uut.num_winners == 1)

def test_single_ballot_poll_1():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll('foo', test_Candidates, 9012, 1)
    for ballot in test_Ballots:
        test_Poll.submit_ballot(ballot)

    assert(run_STV_poll(test_Poll) == {1:["A"]})

def test_single_ballot_poll_2():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll('foo', test_Candidates, 9012, 2)
    for ballot in test_Ballots:
        test_Poll.submit_ballot(ballot)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"]})

def test_single_ballot_poll_3():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll('foo', test_Candidates, 9012, 3)
    for ballot in test_Ballots:
        test_Poll.submit_ballot(ballot)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["C"]})

def test_multiple_ballot_poll_1():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Votes_2 = [Vote("A", 1), Vote("B", 3), Vote("D", 2)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["D"]})

def test_more_winners_than_candidates():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C")]
    test_Poll = Poll('foo', test_Candidates, 9012, 4)
    for ballot in test_Ballots:
        test_Poll.submit_ballot(ballot)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["C"]})

def test_perfect_loser_tie():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Votes_2 = [Vote("A", 1), Vote("B", 2), Vote("D", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["C", "D"]})

def test_imperfect_loser_tie():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Votes_2 = [Vote("A", 1), Vote("B", 2), Vote("D", 3)]
    test_Votes_3 = [Vote("A", 1), Vote("B", 2), Vote("E", 3), Vote("C", 4)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2), Ballot(test_Votes_3, 3)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D"), Candidate("E")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["C"]})

def test_perfect_winner_tie():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2), Vote("C", 3)]
    test_Votes_2 = [Vote("B", 1), Vote("A", 2), Vote("C", 3)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A", "B"], 3:["C"]})

def test_imperfect_winner_tie():
    test_Votes_1 = [Vote("A", 1), Vote("B", 2)]
    test_Votes_2 = [Vote("B", 1), Vote("A", 2)]
    test_Votes_3 = [Vote("C", 1), Vote("A", 2)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2), Ballot(test_Votes_3, 3)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A"], 2:["B"], 3:["C"]})

def test_more_winners_than_allocated():
    test_Votes_1 = [Vote("A", 1)]
    test_Votes_2 = [Vote("B", 1)]
    test_Votes_3 = [Vote("C", 1)]
    test_Ballots = [Ballot(test_Votes_1, 1), Ballot(test_Votes_2, 2), Ballot(test_Votes_3, 3)]
    test_Candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 3)

    assert(run_STV_poll(test_Poll) == {1:["A", "B", "C"]})

