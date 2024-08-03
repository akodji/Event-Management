import streamlit as st
from event_management import EventManagement
import datetime

# Initialize the EventManagement instance
event_manager = EventManagement()

# Define Streamlit application layout
st.title("Event Scheduler and Calendar")

# Create a new event
st.header("Create Event")
with st.form(key="create_event_form"):
    title = st.text_input("Title")
    date = st.date_input("Date", value=datetime.date.today())
    time = st.time_input("Time", value=datetime.datetime.now().time())
    location = st.text_input("Location")
    description = st.text_area("Description")
    priority = st.slider("Priority", min_value=1, max_value=5)
    submit_button = st.form_submit_button("Create Event")

    if submit_button:
        event_id = len(event_manager.viewEvents()) + 1  # Simple ID generation
        event_manager.create_event(event_id, title, date, time, location, description, priority)
        st.success(f"Event '{title}' created successfully!")

# Modify an existing event
st.header("Modify Event")
with st.form(key="modify_event_form"):
    event_id = st.number_input("Event ID", min_value=1)
    attribute = st.selectbox("Attribute to Modify", ["title", "date", "time", "location", "description", "priority"])
    new_value = st.text_input("New Value")
    modify_button = st.form_submit_button("Modify Event")

    if modify_button:
        if attribute in ["date", "time"]:
            try:
                new_value = datetime.datetime.strptime(new_value, "%Y-%m-%d").date() if attribute == "date" else datetime.datetime.strptime(new_value, "%H:%M:%S").time()
            except ValueError:
                st.error("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM:SS for time.")
                new_value = None
        elif attribute == "priority":
            try:
                new_value = int(new_value)
            except ValueError:
                st.error("Priority must be an integer.")
                new_value = None
        
        if new_value is not None:
            updated_event = event_manager.modify_event(event_id, attribute, new_value)
            if updated_event:
                st.success(f"Event ID {event_id} modified successfully!")
            else:
                st.error(f"Event ID {event_id} not found.")

# Delete an event
st.header("Delete Event")
with st.form(key="delete_event_form"):
    delete_id = st.number_input("Event ID to Delete", min_value=1)
    delete_button = st.form_submit_button("Delete Event")

    if delete_button:
        deleted_event = event_manager.delete_event(delete_id)
        if deleted_event:
            st.success(f"Event ID {delete_id} deleted successfully!")
        else:
            st.error(f"Event ID {delete_id} not found.")

# View all events
st.header("View Events")
events = event_manager.viewEvents()
if events:
    for event in events:
        st.subheader(f"Event ID: {event.getID()}")
        st.write(f"**Title**: {event.getTitle()}")
        st.write(f"**Date**: {event.getDate()}")
        st.write(f"**Time**: {event.getTime()}")
        st.write(f"**Location**: {event.getLocation()}")
        st.write(f"**Description**: {event.getDescription()}")
        st.write(f"**Priority**: {event.getPriority()}")
        st.write("---")
else:
    st.write("No events to display.")

# Search events
st.header("Search Events")
search_option = st.selectbox("Search By", ["Title", "Date", "Location"])
search_value = st.text_input("Search Value")
search_button = st.button("Search")

if search_button:
    if search_option == "Title":
        results = event_manager.searchByTitle(search_value)
    elif search_option == "Date":
        try:
            search_value = datetime.datetime.strptime(search_value, "%Y-%m-%d").date()
            results = event_manager
