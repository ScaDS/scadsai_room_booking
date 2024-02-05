import os
import runpy
import sys
from functools import partial

import streamlit as st
import scadsai_room_booking
from scadsai_room_booking._utilities import list_room_bookings_today, book_room
from scadsai_room_booking._config import get_calendar, list_all_rooms

from datetime import timedelta, datetime
from scadsai_room_booking._utilities import round_minutes_to_multiple_of_15

def main() -> None:
    streamlit_script_path = os.path.join(os.path.dirname(scadsai_room_booking.__file__), "_streamlit_script.py")
    sys.argv = ["streamlit", "run", streamlit_script_path ]
    runpy.run_module("streamlit", run_name="__main__")

def list_bookings(calendar, room):
    for booking in list_room_bookings_today(calendar, room):
        st.markdown(f"""
        #### {booking.start.strftime("%H:%M")} - {booking.end.strftime("%H:%M")} 
        ## {booking.description} 
        {booking.owner}

        ---
        """)


def book(room, calendar):
    with st.form(f"Book {room} for today", clear_on_submit=True):
        now = round_minutes_to_multiple_of_15(datetime.now())
        start_time = st.time_input("Start time:", value=now, key='start_time')
        end_time = st.time_input("End time:", value=now + timedelta(hours=1), key='end_time')
        owner = st.text_input("Your name (mandatory):", key='owner')
        description = st.text_input("Description:", key='description')

        def do_booking(room):
            owner = st.session_state.owner
            #room = st.session_state.room
            description = st.session_state.description
            start_time = st.session_state.start_time
            end_time = st.session_state.end_time
            if room is None:
                room = st.session_state.room

            if owner is not None and len(owner) > 2:
                book_room(calendar, room, owner, description, datetime.combine(datetime.today(), start_time),
                          datetime.combine(datetime.today(), end_time), debug=False)

        st.form_submit_button("Book!", on_click=partial(do_booking, room=room))


def streamlit_app():
    import numpy as np
    from skimage.io import imread
    import io

    # hide deploy button
    st.set_page_config(page_title="Room Booking", layout="wide")
    st.markdown("""
        <style>        
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)

    st.image(imread(os.path.join(os.path.dirname(scadsai_room_booking.__file__), "logo.png")), caption="", width=200)


    calendar = get_calendar()

    room = "All" # "A03.41 Schladitzer See" # "All"

    if room is None:
        st.title("ScaDS.AI Room Booking")
        room = st.selectbox("Room:", ["Select"] + list_all_rooms(), key='room')
    elif room != "All":
        st.title(room)

    if room == "All":

        non_empty_rooms = []
        for r in list_all_rooms():
            if len(list_room_bookings_today(calendar, r)) > 0:
                non_empty_rooms.append(r)

        columns = st.columns([1] * len(non_empty_rooms))

        for name, col in zip(non_empty_rooms, columns):

            with col:
               st.markdown(f"# {name}")
               list_bookings(calendar, name)

               if st.button(f"Book " + name.split(" ")[0]):
                   book(name, calendar)


    if room != "Select" and room != "All":

        list_bookings(calendar, room)

        if st.button("Book"):
            book(room, calendar)





if __name__ == "__main__":
    streamlit_app()


