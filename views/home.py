from views.template import Template


class Home(Template):
    def title(self):
        return "Hello Template"

    def message(self):
        return "Template"
