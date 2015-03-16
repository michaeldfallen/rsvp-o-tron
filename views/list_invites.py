from views.template import Template


class Invite(object):
    def url(self):
        return "http://foo"

    def guests(self):
        return "John Smith"


class ListInvites(Template):
    def title(self):
        return "All Invites"

    def invites(self):
        return [
            Invite()
        ]
