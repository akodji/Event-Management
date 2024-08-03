import streamlit as st
import pandas as pd
from datetime import datetime

# Add custom CSS for background image, text styling, and centering the input forms
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url('file:///C:/Users/Anna%20Kodji/OneDrive%20-%20Ashesi%20University/DSA%20Project%20Work/pexels-towfiqu-barbhuiya-3440682-9810172.jpg');
        background-size: cover;
        background-position: center;
        color: white;
    }}
    .title {{
        color: white;
        font-family: 'Arial', sans-serif;
        font-size: 2.5em;
        text-align: center;
        margin: 20px 0;
    }}
    .centered-form {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .form-container {{
        background: rgba(0, 0, 0, 0.7); /* Semi-transparent background for form */
        padding: 20px;
        border-radius: 10px;
        width: 80%;
        max-width: 600px;
        margin: 20px auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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

# Initialize session state
if 'event_map' not in st.session_state:
    st.session_state.event_map = {}
if 'event_list' not in st.session_state:
    st.session_state.event_list = []

# Streamlit UI
st.markdown('<h1 class="title">Event Scheduler and Calendar</h1>', unsafe_allow_html=True)

# Sidebar for commands
with st.sidebar:
    st.header("Commands")
    command = st.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

    if command == "Create Event":
        st.subheader("Create a New Event")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            id = st.text_input("Event ID")
            title = st.text_input("Title")
            date = st.date_input("Date", datetime.now().date())
            time = st.time_input("Time", datetime.now().time())
            location = st.text_input("Location")
            description = st.text_area("Description")
            priority = st.number_input("Priority", min_value=1, max_value=10, value=1)
            if st.button("Create Event"):
                if id.isdigit() and title and location and description:
                    if id not in st.session_state.event_map:
                        new_event = Event(id, title, date, time, location, description, priority)
                        st.session_state.event_map[id] = new_event
                        st.session_state.event_list.append(new_event)
                        st.success("Event created successfully!")
                    else:
                        st.error("Event ID already exists. Please use a different ID.")
                else:
                    if not id.isdigit():
                        st.error("Event ID must be numeric.")
                    else:
                        st.error("Please fill in all required fields.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif command == "Modify Event":
        st.subheader("Modify an Existing Event")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            id = st.text_input("Event ID to Modify")
            
            if id:
                if id.isdigit():
                    if id in st.session_state.event_map:
                        event = st.session_state.event_map[id]
                        with st.form(key='modify_event_form'):
                            new_title = st.text_input("New Title", value=event.title)
                            new_date = st.date_input("New Date", value=event.date)
                            new_time = st.time_input("New Time", value=event.time)
                            new_location = st.text_input("New Location", value=event.location)
                            new_description = st.text_area("New Description", value=event.description)
                            new_priority = st.number_input("New Priority", value=event.priority, min_value=1, max_value=10)
                            
                            submit_button = st.form_submit_button("Modify Event")

                            if submit_button:
                                event.title = new_title
                                event.date = new_date
                                event.time = new_time
                                event.location = new_location
                                event.description = new_description
                                event.priority = new_priority
                                st.session_state.event_map[id] = event  # Update the event in the map
                                st.session_state.event_list[:] = [e for e in st.session_state.event_list if e.id != id]  # Update the event list
                                st.session_state.event_list.append(event)  # Add the updated event back to the list
                                st.success("Event modified successfully!")
                    else:
                        st.error("Event ID not found.")
                else:
                    st.error("Event ID must be numeric.")
            else:
                st.warning("Please enter an Event ID.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif command == "Delete Event":
        st.subheader("Delete an Event")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            id = st.text_input("Event ID to Delete")
            if st.button("Delete Event"):
                if id.isdigit():
                    if id in st.session_state.event_map:
                        st.session_state.event_map.pop(id)
                        st.session_state.event_list[:] = [e for e in st.session_state.event_list if e.id != id]
                        st.success("Event deleted successfully!")
                    else:
                        st.error("Event ID not found.")
                else:
                    st.error("Event ID must be numeric.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif command == "View Events":
        st.subheader("View Events")
        if st.session_state.event_list:
            df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
            st.dataframe(df)
        else:
            st.write("No events to display.")

    elif command == "Search Events":
        st.subheader("Search Events")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
            search_value = st.text_input("Search Value")
            if st.button("Search"):
                if search_attr == "Date":
                    try:
                        search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format is correct
                        filtered_events = [e for e in st.session_state.event_list if e.date == search_date]
                    except ValueError:
                        st.error("Invalid date format. Please use YYYY-MM-DD.")
                        filtered_events = []
                else:
                    filtered_events = [e for e in st.session_state.event_list if getattr(e, search_attr.lower(), "").lower() == search_value.lower()]
                
                if filtered_events:
                    df = pd.DataFrame([e.to_dict() for e in filtered_events])
                    st.dataframe(df)
                else:
                    st.write("No events found.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif command == "Sort Events":
        st.subheader("Sort Events")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            sort_attr = st.selectbox("Sort by Attribute", ["Date", "Title", "Priority"])
            if st.button("Sort"):
                sorted_events = sorted(st.session_state.event_list, key=lambda e: getattr(e, sort_attr.lower()))
                df = pd.DataFrame([e.to_dict() for e in sorted_events])
                st.dataframe(df)
            st.markdown('</div>', unsafe_allow_html=True)

    elif command == "Generate Summary":
        st.subheader("Generate Event Summary")
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            date_range = st.date_input("Date Range", value=(datetime.now().date(), datetime.now().date()))
            start_date, end_date = date_range
            summary = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
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
            st.markdown('</div>', unsafe_allow_html=True)
