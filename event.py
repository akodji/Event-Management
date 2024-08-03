from datetime import datetime

class Event:
    def __init__(self, id, title, date, time, location, description, priority):
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.priority = priority

    def __str__(self):
        return (f"ID: {self.id}, Title: {self.title}, Date: {self.date}, Time: {self.time}, "
                f"Location: {self.location}, Description: {self.description}, Priority: {self.priority}")


