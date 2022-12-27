
class Profile:

    def __init__(self, name="", comment="", active=False):
        self.name = name
        self.comment = comment
        self.active = active

    def __str__(self) -> str:
        x = {
            'name', self.name,
            'comment', self.comment,
            'active', self.active,
        }
        return str(x)

    @staticmethod
    def default_profile():
        p = Profile()
        p.active = False
        p.name = "Default"
        p.comment = ""
        return p