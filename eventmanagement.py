from datetime import datetime
import itertools

class EventManagement:
    def __init__(self):
        self.events = {}
        self.next_id = itertools.count(1)
    
    def create_event():
    st.header("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        event_date = st.date_input("Date", min_value=date(1900, 1, 1), max_value=date(2100, 12, 31))
        event_time = st.time_input("Time", value=time(0, 0))
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.number_input("Priority", min_value=1, max_value=10)

        submit_button = st.form_submit_button("Create Event")

        if submit_button:
            event_management.create_event(id, title, event_date, event_time, location, description, priority)
            st.success("Event created successfully!")

def modify_event():
    st.header("Modify an Existing Event")
    id = st.text_input("Enter Event ID to Modify")
    
    if st.button("Load Event"):
        event = event_management.get_event_by_id(id)
        if event:
            with st.form(key='modify_event_form'):
                title = st.text_input("Title", value=event.title)
                event_date = st.date_input("Date", value=event.date)
                event_time = st.time_input("Time", value=event.time)
                location = st.text_input("Location", value=event.location)
                description = st.text_area("Description", value=event.description)
                priority = st.number_input("Priority", min_value=1, max_value=10, value=event.priority)

                submit_button = st.form_submit_button("Update Event")

                if submit_button:
                    event_management.modify_event(id, title, event_date, event_time, location, description, priority)
                    st.success("Event modified successfully!")
        else:
            st.error("Event not found!")

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

