from datetime import date, time
from event import Event

class EventManagement:
    def __init__(self):
        self.event_map = {}  # Dictionary to store events by ID
        self.event_set = set()  # Set to store events and allow for sorting

    def create_event(self, event_id, title, event_date, event_time, location, description, priority):
        event = Event(event_id, title, event_date, event_time, location, description, priority)
        self.event_map[event_id] = event
        self.event_set.add(event)
        return event

    def modify_event(self, event_id, attribute, new_value):
        event = self.event_map.get(event_id)
        if event is None:
            return False

        self.event_set.remove(event)

        if attribute.lower() == "title":
            event.set_title(new_value)
        elif attribute.lower() == "date":
            event.set_date(date.fromisoformat(new_value))
        elif attribute.lower() == "time":
            event.set_time(time.fromisoformat(new_value))
        elif attribute.lower() == "location":
            event.set_location(new_value)
        elif attribute.lower() == "description":
            event.set_description(new_value)
        else:
            return False

        self.event_set.add(event)
        return True

    def delete_event(self, event_id):
        event = self.event_map.pop(event_id, None)
        if event:
            self.event_set.remove(event)
            return True
        return False

    def view_events(self):
        if not self.event_set:
            return "No events to display."

        events_info = []
        for event in sorted(self.event_set, key=lambda e: (e.get_date(), e.get_time())):
            events_info.append(f"Event ID: {event.get_id()}\n"
                               f"Title: {event.get_title()}\n"
                               f"Date: {event.get_date()}\n"
                               f"Time: {event.get_time()}\n"
                               f"Location: {event.get_location()}\n"
                               f"Description: {event.get_description()}\n"
                               "------------------------")
        return "\n".join(events_info)

    def search_by_title(self, title):
        found = False
        events_info = []
        for event in self.event_set:
            if event.get_title().lower() == title.lower():
                found = True
                events_info.append(f"Event ID: {event.get_id()}\n"
                                   f"Title: {event.get_title()}\n"
                                   f"Date: {event.get_date()}\n"
                                   f"Time: {event.get_time()}\n"
                                   f"Location: {event.get_location()}\n"
                                   f"Description: {event.get_description()}\n"
                                   "------------------------")
        if not found:
            return f"No events found with the title: {title}"
        return "\n".join(events_info)

    def search_by_date(self, event_date):
        found = False
        events_info = []
        for event in self.event_set:
            if event.get_date() == event_date:
                found = True
                events_info.append(f"Event ID: {event.get_id()}\n"
                                   f"Title: {event.get_title()}\n"
                                   f"Date: {event.get_date()}\n"
                                   f"Time: {event.get_time()}\n"
                                   f"Location: {event.get_location()}\n"
                                   f"Description: {event.get_description()}\n"
                                   "------------------------")
        if not found:
            return f"No events found with date: {event_date}"
        return "\n".join(events_info)

    def search_by_location(self, location):
        found = False
        events_info = []
        for event in self.event_set:
            if event.get_location().lower() == location.lower():
                found = True
                events_info.append(f"Event ID: {event.get_id()}\n"
                                   f"Title: {event.get_title()}\n"
                                   f"Date: {event.get_date()}\n"
                                   f"Time: {event.get_time()}\n"
                                   f"Location: {event.get_location()}\n"
                                   f"Description: {event.get_description()}\n"
                                   "------------------------")
        if not found:
            return f"No events found with location: {location}"
        return "\n".join(events_info)

    def sort_by_date(self):
        sorted_events = sorted(self.event_set, key=lambda e: (e.get_date(), e.get_time()))
        if not sorted_events:
            return "No events to display."

        events_info = []
        for event in sorted_events:
            events_info.append(f"Event ID: {event.get_id()}\n"
                               f"Title: {event.get_title()}\n"
                               f"Date: {event.get_date()}\n"
                               f"Time: {event.get_time()}\n"
                               f"Location: {event.get_location()}\n"
                               f"Description: {event.get_description()}\n"
                               "------------------------")
        return "\n".join(events_info)

    def sort_by_title(self):
        sorted_events = sorted(self.event_set, key=lambda e: e.get_title())
        if not sorted_events:
            return "No events to display."

        events_info = []
        for event in sorted_events:
            events_info.append(f"Event ID: {event.get_id()}\n"
                               f"Title: {event.get_title()}\n"
                               f"Date: {event.get_date()}\n"
                               f"Time: {event.get_time()}\n"
                               f"Location: {event.get_location()}\n"
                               f"Description: {event.get_description()}\n"
                               "------------------------")
        return "\n".join(events_info)

    def sort_by_priority(self):
        sorted_events = sorted(self.event_set, key=lambda e: e.get_priority(), reverse=True)
        if not sorted_events:
            return "No events to display."

        events_info = []
        for event in sorted_events:
            events_info.append(f"Event ID: {event.get_id()}\n"
                               f"Title: {event.get_title()}\n"
                               f"Date: {event.get_date()}\n"
                               f"Time: {event.get_time()}\n"
                               f"Location: {event.get_location()}\n"
                               f"Description: {event.get_description()}\n"
                               f"Priority: {event.get_priority()}\n"
                               "------------------------")
        return "\n".join(events_info)

    def generate_summary_by_date(self, event_date):
        found = False
        events_info = []
        for event in self.event_set:
            if event.get_date() == event_date:
                found = True
                events_info.append(f"You have an event booked with event ID: {event.get_id()}\n"
                                   f"Title: {event.get_title()}\n"
                                   f"Date: {event.get_date()}\n"
                                   f"Time: {event.get_time()}\n"
                                   f"Location: {event.get_location()}\n"
                                   f"Description: {event.get_description()}\n"
                                   "------------------------")
        if not found:
            return f"No events found with date: {event_date}"
        return "\n".join(events_info)
