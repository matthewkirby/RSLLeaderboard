class Player:
    def __init__(self, userid, basename, discriminator, rating):
        self.userid = userid
        self.name = f"{basename}#{discriminator}" if discriminator is not None else basename
        self.rating = rating

        # Entry data
        self.lock_entry_data = False
        self.entries = 0
        self.finishes = 0

        # Extra Player Data
        self.public_rating = None


    def joined(self, place):
        if not self.lock_entry_data:
            self.entries += 1
            if place is not None:
                self.finishes += 1
        else:
            print("Attempting to edit race entry data while locked:", self)


    def set_entry_data(self, entries, finishes):
        self.entries = entries
        self.finishes = finishes
        self.lock_entry_data = True


    def export_player_info(self):
        if self.rating is None:
            print("Attempted to export player info without providing a rating:", self)

        mu = self.rating.mu
        sigma = self.rating.sigma
        self.public_rating = round((mu - 2*sigma)*100)
        player_info = {
            "name": self.name,
            "entries": self.entries,
            "finishes": self.finishes,
            "rating": self.public_rating
        }
        return player_info


    def __str__(self):
        if self.public_rating is not None:
            return f"{self.name}: ({self.finishes}/{self.entries}) {self.public_rating}"
        else:
            return f"{self.name}: ({self.finishes}/{self.entries}) {self.rating}"