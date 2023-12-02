import datetime
import os.path
import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def process_events(events):
    data = {}
    date = None

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        hours = (datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)).total_seconds() / 3600
        event_date = datetime.datetime.fromisoformat(start).strftime("%Y-%m-%d")

        if event_date != date:
            if date is not None and len(data[date]) > 100:
                # Adjust events to meet the 100 len requirement
                adjust_events_to_limit(data, date)
            date = event_date
            data[date] = []

        data[date].append({"hours": hours, "summary": event["summary"]})

    # Check the last date
    for i in range(0, 10):
        print(cnt_events(data), i)
        if cnt_events(data) < 100:
            return data
        else:
            data = adjust_events_to_limit(data, i)

    return ValueError


def cnt_events(data):
    cnt = 0
    for date in data:
        cnt += len(data[date])
    return cnt


def adjust_events_to_limit(data, threshold_hours):
    for date in data:
        # Filter out events shorter than the threshold
        data[date] = [event for event in data[date] if event["hours"] > threshold_hours]

    keys_to_delete = []
    for date in data:
        if len(data[date]) == 0:
            keys_to_delete.append(date)

    for key in keys_to_delete:
        del data[key]

    return data


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2023, 12, 31, 23, 59, 59)

        print("Getting the events for the year 2023")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_date.isoformat() + "Z",
                timeMax=end_date.isoformat() + "Z",
                # maxResults=10,
                maxResults=20000,
                singleEvents=True,
                orderBy="startTime",
                fields="items(summary,start,end)",
            )
            .execute()
        )
        events = events_result.get("items", [])

        pprint.pprint(events)

        if not events:
            print("No upcoming events found.")
            return

        # data = {}
        # date = None

        # # Process each event
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     end = event["end"].get("dateTime", event["end"].get("date"))
        #     hours = (datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)).total_seconds() / 3600
        #     event_date = datetime.datetime.fromisoformat(start).strftime("%Y-%m-%d")

        #     # Check if it's a new date
        #     if event_date != date:
        #         if date is not None:
        #             if len(data[date]) == 0:
        #                 del data[date]
        #         date = event_date
        #         data[date] = []

        #     # Append event information as a dictionary
        #     data[date].append({"hours": hours, "summary": event["summary"]})

        # pprint.pprint(data)

        # Process the events
        processed_data = process_events(events)

        # Print the processed data
        pprint.pprint(processed_data)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
