def run_STV_poll(poll): # Pass in a poll
    candidates = []
    for i in poll.ballots:
        for j in i.votes:
            candidates.append(j.candidate)
    return
