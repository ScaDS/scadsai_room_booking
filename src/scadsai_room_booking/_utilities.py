def parse_location(location, summary):
    from ._config import unify_location

    if location is not None and len(location.strip()) > 3:
        return unify_location(location)
    else:
        return unify_location(summary)


def parse_owner(summary):

    summary = summary.replace("Organization:", ",").\
                replace("Organized by:", ","). \
                replace("Contact:", ",")

    if ":" in summary:
        temp = summary.split(":")[-1].strip()
    elif "\\" in summary:
        temp = summary.split("\\")[-1].strip()
    elif "(" in summary:
        temp = summary.split("(")[-1].replace(")", "").strip()
    elif "/" in summary:
        temp = summary.split("/")[-1].strip()
    elif "," in summary:
        temp = summary.split(",")[-1].strip()
    else:
        return summary.strip().split(" ")[-1]

    if "," in temp or ":" in temp or len(temp.split(" ")) > 3:
        return parse_owner(temp)
    else:
        return temp


def list_room_bookings_today(calendar, room):
    from datetime import datetime, timedelta
    from ._room_booking import RoomBooking
    from ._config import unify_location

    start_date = datetime.today().date()

    events = calendar.date_search(start=start_date, end=datetime.today() + timedelta(days=1))

    room_bookings = [RoomBooking(e.data) for e in events]

    room_bookings = [rb for rb in room_bookings if rb.start.date() == datetime.today().date()]

    if room is not None:
        room = unify_location(room)

        selected_room_bookings = [rb for rb in room_bookings if room in rb.room]
    else:
        selected_room_bookings = room_bookings

    sorted_bookings = sorted(selected_room_bookings, key=lambda x: str(x))

    return sorted_bookings


def round_minutes_to_multiple_of_15(dt):

    from datetime import timedelta,datetime

    # Calculate the remainder when dividing the minutes by 15
    minute_remainder = dt.minute % 15

    minute_adjustment = 15 - minute_remainder

    # Create a timedelta with the minute adjustment
    adjustment = timedelta(minutes=minute_adjustment)

    # Add the adjustment to the original datetime
    rounded_dt = dt + adjustment

    return rounded_dt

def parse_description(description, owner, room):
    temp = description.replace(owner, "").\
                       replace(room, "").\
                       replace("()", "").\
                       replace("  ", " ").\
                       replace(", ,", ",").\
                       strip(",").\
                       strip("\\").\
                       strip().\
                       strip(",")

    return temp


def book_room(calendar, room, owner, description, start, end, debug=True):
    from ._config import unify_location

    room_str = unify_location(room)
    start_str = start.strftime("%Y%m%dT%H%M%S")
    end_str = end.strftime("%Y%m%dT%H%M%S")
    summary_escaped = description.replace(",", "\\,")
    summary_str = f"{room_str}, {summary_escaped} ({owner})"

    data = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Sabre//Sabre VObject 4.4.2//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
SUMMARY:{summary_str}
DTSTART:{start_str}
DTEND:{end_str}
DESCRIPTION:{description}
LOCATION:{room_str}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR'
"""
    if debug:
        print(data)
    else:
        calendar.save_event(data)
