from app.views.template import Template


class Step1Start(Template):
    title = "Hello, Guest!"

    def __init__(self, form):
        self.form = form

    def errors(self):
        err = []
        for (key, errorList) in self.form.errors.items():
            for error in errorList:
                err.append({
                    "key": key,
                    "error": error
                })
        return err


class Step2InviteDetails(Template):
    title = "Please join us at our wedding"

    def __init__(self, form):
        self.form = form

    def errors(self):
        return self.form.errors
