import json
import yaml
from random import choice, randint
from hun_date_parser import datetime2text
from datetime import datetime
from time_table import TimeTable


def get_human_friendly_range(daterange, include_date=True):
    include_secondary_date = False
    if daterange.start_datetime.date() != daterange.end_datetime.date():
        include_secondary_date = True

    date_ind = randint(0, 1)
    # time_ind = randint(0, 3)
    time_ind = -1

    if include_date:
        human_friendly_start = f"{datetime2text(daterange.start_datetime, 1)['dates'][date_ind]} " \
                               f"{datetime2text(daterange.start_datetime, 1)['times'][time_ind]}"
    else:
        human_friendly_start = f"{datetime2text(daterange.start_datetime, 1)['times'][time_ind]}"

    if not include_secondary_date:
        human_friendly_end = f"{datetime2text(daterange.end_datetime, 1)['times'][time_ind]}"
    else:
        human_friendly_end = f"{datetime2text(daterange.end_datetime, 1)['dates'][date_ind]} " \
                             f"{datetime2text(daterange.end_datetime, 1)['times'][time_ind]}"

    return human_friendly_start, human_friendly_end


def load_responses():
    with open("response_templates.yml") as f:
        d = yaml.load(f, yaml.FullLoader)

    return d


def get_random_response(responses, label):
    resp = choice(responses[label])
    return resp


def get_available_appointments():
    """
    Loads available appointment list.
    """
    now = datetime.now()  # Get the current date

    with open('test_data.json', 'r') as f:  # Opening test_data
        data = json.load(f)

    # Parsing the test_data into a dictionary
    res = []
    for day in data:
        parsed = {'start_date': datetime.fromisoformat(day['start_date']),
                  'end_date': datetime.fromisoformat(day['end_date'])}

        # Normalizing the data
        if parsed['end_date'] <= now:
            continue
        if parsed['start_date'] <= now:
            parsed['start_date'] = now
        res.append(parsed)

    return res


def get_timetable_in_discussion(tracker):
    time_table_repr = tracker.get_slot('time_table')

    if not time_table_repr:
        time_table = TimeTable(['user_free', 'bot_free', 'last_offered'])
        for rec in get_available_appointments():
            time_table.label_timerange(rec['start_date'], rec['end_date'], 'bot_free')
    else:
        time_table = TimeTable.fromJSON(time_table_repr)

    return time_table
