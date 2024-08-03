from event import Event
import datetime

class EventManagement:
    def __init__(self):
        self.eventSet = set()

    def create_event(self, id, title, date, time, location, description, priority):
        event = Event(id, title, date, time, location, description, priority)
        self.eventSet.add(event)
        return event

    def modify_event(self, event_id, attribute, new_value):
        event = self.find_event_by_id(event_id)
        if event:
            if attribute == "title":
                event.title = new_value
            elif attribute == "date":
                event.date = datetime.datetime.strptime(new_value, "%Y-%m-%d").date()
            elif attribute == "time":
                event.time = datetime.datetime.strptime(new_value, "%H:%M:%S").time()
            elif attribute == "location":
                event.location = new_value
            elif attribute == "description":
                event.description = new_value
            elif attribute == "priority":
                event.priority = int(new_value)
            else:
                raise ValueError("Invalid attribute")
            return event
        else:
            return None

    def delete_event(self, event_id):
        event = self.find_event_by_id(event_id)
        if event:
            self.eventSet.remove(event)
            return event
        else:
            return None

    def viewEvents(self):
        return list(self.eventSet)

    def searchByDate(self, date):
        return [event for event in self.eventSet if event.getDate() == date]

    def searchByTitle(self, title):
        return [event for event in self.eventSet if title.lower() in event.getTitle().lower()]

    def searchByLocation(self, location):
        return [event for event in self.eventSet if location.lower() in event.getLocation().lower()]

    def sort_events(self, attribute):
        if attribute == "date":
            return sorted(self.eventSet, key=lambda e: e.getDate())
        elif attribute == "title":
            return sorted(self.eventSet, key=lambda e: e.getTitle())
        elif attribute == "priority":
            return sorted(self.eventSet, key=lambda e: e.getPriority())
        else:
            raise ValueError("Invalid attribute")

    def find_event_by_id(self, event_id):
        for event in self.eventSet:
            if event.getID() == event_id:
                return event
        return None
