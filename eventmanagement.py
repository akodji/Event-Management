from datetime import datetime
import itertools

class EventManagement:
    def __init__(self):
        self.events = {}
        self.next_id = itertools.count(1)
    
    def create_event(self, title, date, time, location, description, priority):
        event_id = str(next(self.next_id))
        event = Event(event_id, title, date, time, location, description, priority)
        self.events[event_id] = event
        print(f"Event created: {event}")

    def modify_event(self, event_id, attribute, new_value):
        if event_id in self.events:
            event = self.events[event_id]
            if attribute == "title":
                event.title = new_value
            elif attribute == "date":
                event.date = datetime.strptime(new_value, "%Y-%m-%d").date()
            elif attribute == "time":
                event.time = datetime.strptime(new_value, "%H:%M").time()
            elif attribute == "location":
                event.location = new_value
            elif attribute == "description":
                event.description = new_value
            elif attribute == "priority":
                event.priority = int(new_value)
            else:
                print("Invalid attribute.")
                return
            print(f"Event modified: {event}")
        else:
            print("Event ID not found.")

    def delete_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]
            print(f"Event with ID {event_id} deleted.")
        else:
            print("Event ID not found.")

    def view_events(self, filter_by=None):
        for event in self.events.values():
            if not filter_by or (filter_by in event.date.isoformat()):
                print(event)
    
    def search_event(self, attribute, value):
        found = False
        for event in self.events.values():
            if (attribute == "title" and value.lower() in event.title.lower()) or \
               (attribute == "date" and value == event.date.isoformat()) or \
               (attribute == "location" and value.lower() in event.location.lower()):
                print(event)
                found = True
        if not found:
            print("No events found.")
    
    def sort_events(self, attribute):
        sorted_events = sorted(self.events.values(), key=lambda e: getattr(e, attribute))
        for event in sorted_events:
            print(event)
    
    def generate_summary(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        found = False
        for event in self.events.values():
            if start <= event.date <= end:
                print(event)
                found = True
        if not found:
            print("No events found in the specified date range.")
