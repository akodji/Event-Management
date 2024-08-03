import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set banner image
def set_banner_image(banner_image):
    banner_base64 = get_base64_of_bin_file(banner_image)
    st.markdown(
        f"""
        <style>
        .banner {{
            background-image: url(data:image/png;base64,{banner_base64});
            background-size: cover;
            background-position: center;
            padding: 150px 0;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set banner image
set_banner_image('event.jpg')  # replace with your image file name

# Create a banner container without the title
st.markdown(
    """
    <div class="banner">
    </div>
    """,
    unsafe_allow_html=True
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background: white;
    }
    .sidebar .sidebar-content {
        background: rgba(255,255,255,0.8);
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .Widget>label {
        color: black;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput>div>div>input {
        color: black;
    }
    .stSelectbox>div>div>select {
        color: black;
    }
    .banner {
        text-align: center;
    }
    footer {
        color: black;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: rgba(0,0,0,0.1);
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add your main app content here
# For example:
# st.title("Create Event")
# event_name = st.text_input("Event Name")
# event_date = st.date_input("Event Date")
# ...


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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")



import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .sidebar .sidebar-content h1 {
        color: #000000;
    }
    .title {
        text-align: center;
        color: white;
        font-family: 'Arial Narrow', sans-serif;
        font-weight: bold;
        font-size: 36px;
    }
    footer {
        color: white;
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: #333;
        font-size: 12px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and header
st.markdown('<p class="title">Event Scheduler and Calendar</p>', unsafe_allow_html=True)

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
st.sidebar.header("Commands")
command = st.sidebar.selectbox("Choose a command", ["Create Event", "Modify Event", "Delete Event", "View Events", "Search Events", "Sort Events", "Generate Summary"])

if command == "Create Event":
    st.subheader("Create a New Event")
    with st.form(key='create_event_form'):
        id = st.text_input("Event ID")
        title = st.text_input("Title")
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
        location = st.text_input("Location")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submit_button = st.form_submit_button("Create Event")
        if submit_button:
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

elif command == "Modify Event":
    st.subheader("Modify an Existing Event")
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
                    new_priority = st.selectbox("New Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(event.priority))
                    
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

elif command == "Delete Event":
    st.subheader("Delete an Event")
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

elif command == "View Events":
    st.subheader("View Events")
    if st.session_state.event_list:
        df = pd.DataFrame([e.to_dict() for e in st.session_state.event_list])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Search Events":
    st.subheader("Search Events")
    search_attr = st.selectbox("Search by Attribute", ["Title", "Date", "Location"])
    search_value = st.text_input("Search Value")
    
    if st.button("Search"):
        found_events = []
        if search_attr == "Date":
            try:
                search_date = datetime.strptime(search_value, "%Y-%m-%d").date()  # Ensure date format
                found_events = [e for e in st.session_state.event_list if e.date == search_date]
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            found_events = [e for e in st.session_state.event_list if search_value.lower() in getattr(e, search_attr.lower()).lower()]

        if found_events:
            df = pd.DataFrame([e.to_dict() for e in found_events])
            st.dataframe(df)
        else:
            st.write("No events found matching the criteria.")

elif command == "Sort Events":
    st.subheader("Sort Events")
    sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])
    
    if sort_by == "Date":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: (e.date, e.time))
    elif sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_events = sorted(st.session_state.event_list, key=lambda e: priority_order[e.priority])
    elif sort_by == "Title":
        sorted_events = sorted(st.session_state.event_list, key=lambda e: e.title.lower())  # Sorting by title alphabetically
    
    if sorted_events:
        df = pd.DataFrame([e.to_dict() for e in sorted_events])
        st.dataframe(df)
    else:
        st.write("No events to display.")

elif command == "Generate Summary":
    st.subheader("Generate Summary of Events")
    
    # Input date range for summary
    start_date = st.date_input("Start Date", datetime.now().date())
    end_date = st.date_input("End Date", datetime.now().date())

    if st.button("Generate Summary"):
        if start_date <= end_date:
            # Filter events based on date range
            summary_events = [e for e in st.session_state.event_list if start_date <= e.date <= end_date]
            
            if summary_events:
                for event in summary_events:
                    st.write(f"**Event ID:** {event.id}")
                    st.write(f"**Title:** {event.title}")
                    st.write(f"**Date:** {event.date.strftime('%Y-%m-%d')}")
                    st.write(f"**Time:** {event.time.strftime('%H:%M:%S')}")
                    st.write(f"**Location:** {event.location}")
                    st.write(f"**Description:** {event.description}")
                    st.write(f"**Priority:** {event.priority}")
                    st.write("------------------------")
            else:
                st.write("No events found in the specified date range.")
        else:
            st.error("Start date must be on or before end date.")




