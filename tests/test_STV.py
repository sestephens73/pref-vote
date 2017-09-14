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

def test_run_STV_poll():
    test_Votes_1 = [Vote("Sean", 1), Vote("Neil", 2)]
    test_Votes_2 = [Vote("John", 2), Vote("Cob", 1)]
    test_Ballots = [Ballot(test_Votes_1, 1234), Ballot(test_Votes_2, 5678)]
    test_Candidates = [Candidate("Sean"), Candidate("Neil"), Candidate("John"), Candidate("Cob")]
    test_Poll = Poll(test_Candidates, test_Ballots, 9012, 1)

    run_STV_poll(test_Poll)

    assert(test_Poll.candidates["Sean"].total_votes == 1)
    assert(test_Poll.candidates["Neil"].total_votes == 0)
    assert(test_Poll.candidates["John"].total_votes == 0)
    assert(test_Poll.candidates["Cob"].total_votes == 1)

    assert(test_Poll.ballots[0].votes[1].counted == True)
    assert(test_Poll.ballots[0].votes[2].counted == False)
    assert(test_Poll.ballots[1].votes[2].counted == False)
    assert(test_Poll.ballots[1].votes[1].counted == True)
