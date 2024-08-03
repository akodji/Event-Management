from datetime import date, time

class Event:
    def __init__(self, event_id, title, event_date, event_time, location, description, priority):
        self.id = event_id
        self.title = title
        self.date = event_date
        self.time = event_time
        self.location = location
        self.description = description
        self.priority = priority

    def set_title(self, title):
        self.title = title

    def set_date(self, event_date):
        self.date = event_date

    def set_time(self, event_time):
        self.time = event_time

    def set_location(self, location):
        self.location = location

    def set_description(self, description):
        self.description = description

    def set_priority(self, priority):
        self.priority = priority

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_location(self):
        return self.location

    def get_description(self):
        return self.description

    def get_priority(self):
        return self.priority
