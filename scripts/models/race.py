from models.entrant import Entrant

class Race:
    def __init__(self, slug, end_time, results):
        self.slug = slug
        self.end_time = end_time
        self.entrants = [Entrant(entry[0], entry[1], entry[2]) for entry in results]