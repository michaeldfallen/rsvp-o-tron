from flask_stache import render_view


class Home(object):
    def message(self):
        return "Mustache"

    def render(self):
        return render_view(self)
