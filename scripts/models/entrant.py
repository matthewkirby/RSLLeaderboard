class Entrant:
    def __init__(self, primary_key, userid, place, rating_before=None, rating_after=None):
        self.primary_key = primary_key
        self.userid = userid
        self.place = place
        self.rating_before = rating_before
        self.rating_after = rating_after

    def __str__(self):
        return f"Entrant({self.userid}) finished {self.place}: {self.rating_before} > {self.rating_after}"