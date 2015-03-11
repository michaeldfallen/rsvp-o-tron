from flask_stache import render_view


class Template(object):

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
            self.content = render_view(sub_template)

    @classmethod
    def render(sub_template_clazz):
        return render_view(
            Template(sub_template_clazz())
        )
