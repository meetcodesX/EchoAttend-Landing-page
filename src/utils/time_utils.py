import streamlit as st
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def to_ist(ts):
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    try:
        dt = dt.astimezone(ZoneInfo("Asia/Kolkata"))
    except ZoneInfoNotFoundError:
        st.error("Timezone database (tzdata) not available — showing UTC instead.")
    return dt