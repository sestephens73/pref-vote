from pref_vote.poll import Poll, Candidate

def test_Vote():
    pass

def test_Ballot():
    pass

def test_Candidate():
    uut = Candidate("Neil")
    assert(uut.name == "Neil")
    assert(uut.total_votes == 0)
    assert(uut.has_won == False)
    assert(uut.is_eliminated == False)

def test_Poll():
    pass

def test_run_STV_poll():
    pass
