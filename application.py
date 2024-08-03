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
        event_id = len(event_manager.view_events()) + 1  # Simple ID generation
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
        try:
            if attribute in ["date", "time"]:
                new_value = datetime.datetime.strptime(new_value, "%Y-%m-%d").date() if attribute == "date" else datetime.datetime.strptime(new_value, "%H:%M:%S").time()
            elif attribute == "priority":
                new_value = int(new_value)
            updated_event = event_manager.modify_event(event_id, attribute, new_value)
            if updated_event:
                st.success(f"Event ID {event_id} modified successfully!")
            else:
                st.error(f"Event ID {event_id} not found.")
        except ValueError as e:
            st.error(f"Invalid input: {e}")

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
events = event_manager.view_events()
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
    try:
        if search_option == "Title":
            results = event_manager.search_by_title(search_value)
        elif search_option == "Date":
            search_value = datetime.datetime.strptime(search_value, "%Y-%m-%d").date()
            results = event_manager.search_by_date(search_value)
        elif search_option == "Location":
            results = event_manager.search_by_location(search_value)

        if results:
            for event in results:
                st.subheader(f"Event ID: {event.getID()}")
                st.write(f"**Title**: {event.getTitle()}")
                st.write(f"**Date**: {event.getDate()}")
                st.write(f"**Time**: {event.getTime()}")
                st.write(f"**Location**: {event.getLocation()}")
                st.write(f"**Description**: {event.getDescription()}")
                st.write(f"**Priority**: {event.getPriority()}")
                st.write("---")
        else:
            st.write("No matching events found.")
    except ValueError as e:
        st.error(f"Invalid date format: {e}")

# Sort events
st.header("Sort Events")
sort_option = st.selectbox("Sort By", ["Date", "Title", "Priority"])
sort_button = st.button("Sort")

if sort_button:
    sorted_events = event_manager.sort_events(sort_option.lower())
    if sorted_events:
        for event in sorted_events:
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
