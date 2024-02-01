class RoomBooking():
    def __init__(self, event_data: str):
        import re
        from ._utilities import parse_location, parse_owner, parse_description
        from datetime import datetime, timedelta

        self.room = None
        self.owner = None
        self.description = None
        self.start = None
        self.end = None

        # The text block provided
        text = event_data

        # Patterns for each piece of information
        location_pattern = r'LOCATION:(.+)\n'
        summary_pattern = r'SUMMARY:(.+)\n'
        description_pattern = r'DESCRIPTION:(.+)\n'
        start_date_time_pattern = r'DTSTART:(\d+T\d+Z)\n'
        end_date_time_pattern = r'DTEND:(\d+T\d+Z)\n'

        # Extracting each piece of information using the defined patterns
        location_match = re.search(location_pattern, text)
        summary_match = re.search(summary_pattern, text)
        description_match = re.search(description_pattern, text)
        start_date_time_match = re.search(start_date_time_pattern, text)
        end_date_time_match = re.search(end_date_time_pattern, text)

        # Extracting and printing the matched text for each piece of information
        location = location_match.group(1) if location_match else None
        summary = summary_match.group(1) if summary_match else None
        description = description_match.group(1) if description_match else None
        start_date_time = start_date_time_match.group(1) if start_date_time_match else None
        end_date_time = end_date_time_match.group(1) if end_date_time_match else None

        # Reformating the datetime for readability, if they were found
        if start_date_time:
            start_date_time = start_date_time[:8] + ' ' + start_date_time[9:13]

        if end_date_time:
            end_date_time = end_date_time[:8] + ' ' + end_date_time[9:13]

        # print(f"Location: {location}")
        # print(f"Summary: {summary}")
        # print(f"Start: {start_date_time}")
        # print(f"End: {end_date_time}")

        if description is not None:
            if description in summary:
                description = None

        self.room = parse_location(location, summary)
        if description is not None:
            self.owner = parse_owner(summary + description)
        else:
            self.owner = parse_owner(summary)
        self.start = datetime.strptime(start_date_time, "%Y%m%d %H%M")
        self.end = datetime.strptime(end_date_time, "%Y%m%d %H%M")

        self.description = parse_description(summary, self.owner, self.room)
        if self.description is None or len(self.description) < 3:
            self.description = "Undefined meeting"

    def __str__(self):
        return f"RoomBooking {self.start} - {self.end} {self.room}: {self.description} ({self.owner})"

    def __repr__(self):
        return str(self)
