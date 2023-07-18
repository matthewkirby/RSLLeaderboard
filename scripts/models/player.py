class Player:
    def __init__(self, userid, basename, discriminator, rating):
        self.userid = userid
        self.name = f"{basename}#{discriminator}" if discriminator is not None else basename
        self.rating = rating

        self.entries = 0
        self.finishes = 0

    def joined(self, place):
        self.entries += 1
        if place is not None:
            self.finishes += 1