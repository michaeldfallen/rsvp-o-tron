from app.views.template import Template
from app.forms import FormHandler
from itertools import groupby


class Step1Start(Template, FormHandler):
    title = "Hello, Guest!"
    page_type = "big-page"

    def __init__(self, form):
        self.form = form


class Step2InviteDetails(Template):
    title = "Please join us at our wedding"

    def __init__(self, invite):
        self.invite = invite

    def guest_list(self, pred=lambda x: x):
        def last_name(o):
            return o.last_name

        def guest_name(guest):
            return guest.first_name

        def concat_and_at_end(l):
            first_n = ", ".join(l[:-1])
            last = "".join(l[-1:])
            all_not_empty = filter(None, [first_n, last])
            return " and ".join(all_not_empty)

        def concat_family(family_name, guests):
            names = list(map(guest_name, guests))
            return concat_and_at_end(names) + " " + family_name

        filtered = filter(pred, self.invite.guests)

        sorted_names = sorted(filtered, key=last_name)

        families = groupby(sorted_names, last_name)
        guest_names = list(map(lambda x: concat_family(*x), families))

        return concat_and_at_end(guest_names)

    def secondary_guests(self):
        def is_secondary(o):
            return o.is_primary is False

        return self.guest_list(is_secondary)

    def primary_guests(self):
        def is_primary(o):
            return o.is_primary is True

        return self.guest_list(is_primary)

    def has_primary(self):
        return self.primary_guests() is not ""

    def has_secondary(self):
        return self.secondary_guests() is not ""


class Step3Respond(Template, FormHandler):
    title = "Will you attend?"

    def __init__(self, form, guest):
        self.guest = guest
        self.form = form


class Step4MenuChoices(Template, FormHandler):
    title = "What would you like for dinner"

    def __init__(self, form, guest):
        self.guest = guest
        self.form = form


class ConfirmStep(Template):
    title = "Confirm your RSVP"

    def __init__(self, rsvps):
        self.rsvps = rsvps


class FinishedStep(Template):
    title = "Thanks for RSVPing"

    def __init__(self, rsvps, already_finished=False, has_room=False):
        self.rsvps = rsvps
        self.already_finished = already_finished
        self.has_room = has_room

    def guest_list(self, pred=lambda x: x):
        def last_name(o):
            return o.last_name

        def guest_name(guest):
            return guest.first_name

        def concat_and_at_end(l):
            first_n = ", ".join(l[:-1])
            last = "".join(l[-1:])
            all_not_empty = filter(None, [first_n, last])
            return " and ".join(all_not_empty)

        def concat_family(family_name, guests):
            names = list(map(guest_name, guests))
            return concat_and_at_end(names) + " " + family_name

        filtered_rsvps = filter(pred, self.rsvps)

        guests = list(map(lambda x: x.guest, filtered_rsvps))

        sorted_names = sorted(guests, key=last_name)

        families = groupby(sorted_names, last_name)
        guest_names = list(map(lambda x: concat_family(*x), families))

        return concat_and_at_end(guest_names)

    def guest_names_avoiding(self):
        return self.guest_list(lambda rsvp: not rsvp.attending)

    def guest_names_attending(self):
        return self.guest_list(lambda rsvp: rsvp.attending)

    def people_attending(self):
        def are_attending(o):
            return o.attending

        return filter(are_attending, self.rsvps)

    def are_people_attending(self):
        return len(list(self.people_attending())) != 0

    def people_avoiding(self):
        def are_not_attending(o):
            return not o.attending

        return filter(are_not_attending, self.rsvps)

    def are_people_avoiding(self):
        return len(list(self.people_avoiding())) != 0

    def menu_choices(self):
        def readable_menu_choice(rsvp):
            choice = ""
            if rsvp.menu_choice == "beef":
                choice = "Roast sirloin of beef"
            elif rsvp.menu_choice == "turkey":
                choice = "Stuffed turkey and ham"
            elif rsvp.menu_choice == "vegetarian":
                choice = "Vegetable tarte tatin"

            return {"name": rsvp.name, "choice": choice}

        return list(map(readable_menu_choice, self.people_attending()))

    def only_one_guest(self):
        return len(list(self.people_attending())) == 1

    def more_than_one_guest(self):
        return not self.only_one_guest()
