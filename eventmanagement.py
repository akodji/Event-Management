# event_management.py

from datetime import datetime

class Event:
    def __init__(self, event_id, title, date, time, location, description, priority):
        self.event_id = event_id
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.priority = priority

    def getID(self):
        return self.event_id

    def getTitle(self):
        return self.title

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getLocation(self):
        return self.location

    def getDescription(self):
        return self.description

    def getPriority(self):
        return self.priority

    def setTitle(self, title):
        self.title = title

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def setLocation(self, location):
        self.location = location

    def setDescription(self, description):
        self.description = description

    def setPriority(self, priority):
        self.priority = priority

class EventManagement:
    def __init__(self):
        self.events = {}

    def create_event(self, event_id, title, date, time, location, description, priority):
        if event_id not in self.events:
            self.events[event_id] = Event(event_id, title, date, time, location, description, priority)
            return True
        return False

    def modify_event(self, event_id, attribute, new_value):
        event = self.events.get(event_id)
        if event:
            if attribute == "title":
                event.setTitle(new_value)
            elif attribute == "date":
                event.setDate(new_value)
            elif attribute == "time":
                event.setTime(new_value)
            elif attribute == "location":
                event.setLocation(new_value)
            elif attribute == "description":
                event.setDescription(new_value)
            elif attribute == "priority":
                event.setPriority(new_value)
            return True
        return False

    def delete_event(self, event_id):
        return self.events.pop(event_id, None) is not None

    def view_events(self):
        return list(self.events.values())

    def search_by_title(self, title):
        return [event for event in self.events.values() if event.getTitle() == title]

    def search_by_date(self, date):
        return [event for event in self.events.values() if event.getDate() == date]

    def search_by_location(self, location):
        return [event for event in self.events.values() if event.getLocation() == location]

    def sort_events(self, attribute):
        if attribute == "date":
            return sorted(self.events.values(), key=lambda e: e.getDate())
        elif attribute == "title":
            return sorted(self.events.values(), key=lambda e: e.getTitle())
        elif attribute == "priority":
            return sorted(self.events.values(), key=lambda e: e.getPriority())
        return []
