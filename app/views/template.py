from flask import url_for
from flask_stache import render_view


class Template(object):
    page_type = ""

    """
    Inherit this class to be able to render a template

    Usage:
        class Foo(Template)

        Foo.render()
    """

    def __init__(self, sub_template=None):
        """

        :sub_template: Optional subtemplate to render content from

        """
        if sub_template is not None:
            self.title = sub_template.title
            self.page_type = sub_template.page_type
            self.main_css = url_for('static', filename='main.css')
            self.content = render_view(sub_template)

    def render(self):
        return render_view(
            Template(self)
        )
