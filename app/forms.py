class FormHandler(object):

    def errors(self):
        err = []
        for (key, errorList) in self.form.errors.items():
            for error in errorList:
                err.append({
                    "key": key,
                    "error": error
                })
        return err
