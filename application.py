import streamlit as st
from event_management import EventManagement
from event import Event
import datetime

# Initialize EventManagement
event_manager = EventManagement()

def add_event():
    st.header("Create Event")
    title = st.text_input("Title")
    date = st.date_input("Date", min_value=datetime.date.today())
    time = st.time_input("Time")
    location = st.text_input("Location")
    description = st.text_area("Description")
    priority = st.number_input("Priority", min_value=1, max_value=10, value=1)
    
    if st.button("Add Event"):
        event_id = f"{date}-{time}"  # Simple ID based on date and time
        event = event_manager.create_event(
            id=event_id,
            title=title,
            date=date,
            time=time,
            location=location,
            description=description,
            priority=priority
        )
        st.success(f"Event '{title}' added!")

def view_events():
    st.header("View Events")
    filter_option = st.selectbox("Filter by", ["All", "Date", "Title", "Location"])
    
    if filter_option == "Date":
        date_filter = st.date_input("Select Date", min_value=datetime.date.today())
        events = event_manager.searchByDate(date_filter)
    elif filter_option == "Title":
        title_filter = st.text_input("Enter Title")
        events = event_manager.searchByTitle(title_filter)
    elif filter_option == "Location":
        location_filter = st.text_input("Enter Location")
        events = event_manager.searchByLocation(location_filter)
    else:
        events = event_manager.viewEvents()  # View all events

    if events:
        for event in events:
            st.write(f"ID: {event.getID()}")
            st.write(f"Title: {event.getTitle()}")
            st.write(f"Date: {event.getDate()}")
            st.write(f"Time: {event.getTime()}")
            st.write(f"Location: {event.getLocation()}")
            st.write(f"Description: {event.getDescription()}")
            st.write(f"Priority: {event.getPriority()}")
            st.write("---")
    else:
        st.write("No events found.")

st.sidebar.title("Event Scheduler")
option = st.sidebar.selectbox("Select an action", ["Create Event", "View Events"])

if option == "Create Event":
    add_event()
elif option == "View Events":
    view_events()
