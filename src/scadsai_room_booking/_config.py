def unify_location(location:str):
    temp = location.upper().\
            replace(".", "").\
            replace(" ", "").\
            replace("-", "")
    if "A0328" in temp or "MARKLEEBERGER" in temp:
        return "A03.28 Markleeberger See"
    elif "D0339" in temp or "COSPUDENER" in temp:
        return "D03.39 Cospudener See"
    elif "A0306" in temp or "LIVING" in temp:
        return "A03.06 Living Lab"
    elif "A0307" in temp or "BIGSEMINAR" in temp or "LARGESEMINAR" in temp or "ZWENKAUER" in temp:
        return "A03.07 Big Seminar Room (Zwenkauer See)"
    elif "A0321" in temp or "KULKWITZER" in temp:
        return "A03.21 Kulkwitzer See"
    elif "A0341" in temp:
        return "A03.41 Schladitzer See"
    else:
        return location


def list_all_rooms():
    return [
        unify_location("A0328"),
        unify_location("D0339"),
        unify_location("LIVING"),
        unify_location("A0307"),
        unify_location("A0321"),
        unify_location("A0341"),
    ]


def get_calendar():
    import os
    import caldav

    url = os.environ.get("SCADSAI_ROOM_CALENDAR")
    username = os.environ.get("SCADSAI_ROOM_USERNAME")
    password = os.environ.get("SCADSAI_ROOM_API_TOKEN")

    client = caldav.DAVClient(url=url, username=username, password=password)
    calendar = client.calendar(url=url)

    return calendar