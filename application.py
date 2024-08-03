import streamlit as st
import pandas as pd
from datetime import datetime

# Define your Event class
class Event:
    def __init__(self, id, title, date, time, location, description, priority):
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.priority = priority

    def to_dict(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Date": self.date,
            "Time": self.time,
            "Location": self.location,
            "Description": self.description,
            "Priority": self.priority
        }

# In-memory data structures
event_map = {}
event_list = []

# Streamlit UI
st.title("Event Scheduler and Calendar")

# Sidebar for commands
with st.sidebar:
    st.header("Commands")
    command = st.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])
    
    if command == "Create Event":
        st.subheader("Create a New Event")
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.number_input("Priority", min_value=1, max_value=10, value=1)
        if st.button("Create Event"):
            if id and title and location and description:
                new_event = Event(id, title, date, time, location, description, priority)
                event_map[id] = new_event
                event_list.append(new_event)
                st.success("Event created successfully!")
            else:
                st.error("Please fill in all required fields.")

    elif command == "Modify Event":
        st.subheader("Modify an Existing Event")
        id = st.text_input("Event ID to Modify")
        if id in event_map:
            event = event_map[id]
            new_title = st.text_input("New Title", value=event.title)
            new_date = st.date_input("New Date", value=event.date)
            new_time = st.time_input("New Time", value=event.time)
            new_location = st.text_input("New Location", value=event.location)
            new_description = st.text_area("New Description", value=event.description)
            new_priority = st.number_input("New Priority", value=event.priority, min_value=1, max_value=10)
            
            if st.button("Modify Event"):
                event.title = new_title
                event.date = new_date
                event.time = new_time
                event.location = new_location
                event.description = new_description
                event.priority = new_priority
                st.success("Event modified successfully!")
        else:
            st.error("Event ID not found.")

    elif command == "Delete Event":
        st.subheader("Delete an Event")
        id = st.text_input("Event ID to Delete")
        if st.button("Delete Event"):
            if id in event_map:
                event_map.pop(id)
                event_list[:] = [e for e in event_list if e.id != id]
                st.success("Event deleted successfully!")
            else:
                st.error("Event ID not found.")

    elif command == "View Events":
        st.subheader("View Events")
        if event_list:
            df = pd.DataFrame([e.to_dict() for e in event_list])
            st.dataframe(df)
        else:
            st.write("No events to display.")

    elif command == "Search Events":
        st.subheader("Search Events")
        search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
        search_value = st.text_input("Search Value")
        if st.button("Search"):
            filtered_events = [e for e in event_list if getattr(e, search_attr.lower(), "").lower() == search_value.lower()]
            if filtered_events:
                df = pd.DataFrame([e.to_dict() for e in filtered_events])
                st.dataframe(df)
            else:
                st.write("No events found.")

    elif command == "Sort Events":
        st.subheader("Sort Events")
        sort_attr = st.selectbox("Sort by Attribute", ["Date", "Title", "Priority"])
        if st.button("Sort"):
            sorted_events = sorted(event_list, key=lambda e: getattr(e, sort_attr.lower()))
            df = pd.DataFrame([e.to_dict() for e in sorted_events])
            st.dataframe(df)

    elif command == "Generate Summary":
        st.subheader("Generate Event Summary")
        date_range = st.date_input("Date Range", value=(datetime.now().date(), datetime.now().date()))
        start_date, end_date = date_range
        summary = [e for e in event_list if start_date <= e.date <= end_date]
        if summary:
            for event in summary:
                st.write(f"Event ID: {event.id}")
                st.write(f"Title: {event.title}")
                st.write(f"Date: {event.date}")
                st.write(f"Time: {event.time}")
                st.write(f"Location: {event.location}")
                st.write(f"Description: {event.description}")
                st.write(f"Priority: {event.priority}")
                st.write("-------------")
        else:
            st.write("No events found in the specified date range.")
