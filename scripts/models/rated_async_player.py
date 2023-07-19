class RatedAsyncPlayer:
    def __init__(self, fullname, userid, ruleset):
        self.name = fullname.split("#")[0].strip()
        self.discriminator = None
        self.userid = userid
        self.ruleset = ruleset # Usage not yet implemented

        if len(fullname.split("#")) > 1:
            self.discriminator = fullname.split("#")[1].strip()

        self.done = False
        self.time = None
        self.media = None # Usage not yet implemented
        self.place = None

    def rtgg_style_output(self):
        entrant = {
            'user': {
                'id': self.userid,
                'name': self.name,
                'discriminator': self.discriminator,
                'url': f"/user/{self.userid}",
                'twitch_display_name': None,
                'twitch_channel': None
            },
            'status': {
                'value': "done" if self.done else "dnf"
            },
            'finish_time': self.time,
            'place': self.place,
            'comment': None
        }
        return entrant