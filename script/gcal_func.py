import datetime
import os.path
import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def process_events(events):
    data = {}
    date = None

    for event in events:
        event_date = extract_event_date(event)
        hours = calculate_event_duration(event)

        if event_date != date:
            manage_data_for_new_date(data, date)
            date = event_date
            data[date] = []

        data[date].append({"hours": hours, "summary": event["summary"]})

    check_data_limit(data)
    return data


def extract_event_date(event):
    start = event["start"].get("dateTime", event["start"].get("date"))
    return datetime.datetime.fromisoformat(start).strftime("%Y-%m-%d")


def calculate_event_duration(event):
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    return (datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)).total_seconds() / 3600


def manage_data_for_new_date(data, date):
    if date is not None and len(data[date]) > 100:
        adjust_events_to_limit(data, date)


def check_data_limit(data):
    for i in range(10):
        print(cnt_events(data), i)
        if cnt_events(data) < 100:
            break
        data = adjust_events_to_limit(data, i)
    else:
        raise ValueError("Data limit exceeded")


def cnt_events(data):
    return sum(len(events) for events in data.values())


def adjust_events_to_limit(data, threshold_hours):
    for date in list(data):
        data[date] = [event for event in data[date] if event["hours"] > threshold_hours]
        if not data[date]:
            del data[date]

    return data


def authenticate_google_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        creds = refresh_or_create_credentials(creds)
    return creds


def refresh_or_create_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds


def main():
    try:
        creds = authenticate_google_calendar()
        service = build("calendar", "v3", credentials=creds)
        events = fetch_calendar_events(service)
        pprint.pprint(process_events(events))
    except HttpError as error:
        print(f"An error occurred: {error}")


def fetch_calendar_events(service):
    print("Getting the events for the year 2023")
    start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2023, 12, 31, 23, 59, 59)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_date.isoformat() + "Z",
        timeMax=end_date.isoformat() + "Z",
        maxResults=20000,
        singleEvents=True,
        orderBy="startTime",
        fields="items(summary,start,end)"
    ).execute()
    events = events_result.get("items", [])
    pprint.pprint(events)
    if not events:
        print("No upcoming events found.")
        return []
    return events


if __name__ == "__main__":
    main()
