from datetime import datetime, date, time
import itertools

class EventManagement:
    def __init__(self):
        self.events = {}
        self.next_id = itertools.count(1)
    
    def create_event(self, title, event_date, event_time, location, description, priority):
        id = next(self.next_id)
        event = {
            'id': id,
            'title': title,
            'date': event_date,
            'time': event_time,
            'location': location,
            'description': description,
            'priority': priority
        }
        self.events[id] = event
        return id

    def modify_event(self, id, title=None, event_date=None, event_time=None, location=None, description=None, priority=None):
        event = self.events.get(id)
        if event:
            if title is not None:
                event['title'] = title
            if event_date is not None:
                event['date'] = event_date
            if event_time is not None:
                event['time'] = event_time
            if location is not None:
                event['location'] = location
            if description is not None:
                event['description'] = description
            if priority is not None:
                event['priority'] = priority
            return True
        return False

    def delete_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]
            return True
        return False

    def get_event_by_id(self, event_id):
        return self.events.get(event_id)

    def view_events(self, filter_by=None):
        filtered_events = [event for event in self.events.values() if not filter_by or filter_by in event['date'].isoformat()]
        return filtered_events
    
    def search_event(self, attribute, value):
        found = [event for event in self.events.values() if (attribute == "title" and value.lower() in event['title'].lower()) or
                 (attribute == "date" and value == event['date'].isoformat()) or
                 (attribute == "location" and value.lower() in event['location'].lower())]
        return found

    def sort_events(self, attribute):
        sorted_events = sorted(self.events.values(), key=lambda e: e[attribute])
        return sorted_events
    
    def generate_summary(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        summary_events = [event for event in self.events.values() if start <= event['date'] <= end]
        return summary_events
