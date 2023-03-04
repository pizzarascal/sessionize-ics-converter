import argparse
import os
import json
import uuid
from datetime import datetime   

ICS_HEADER = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:convert.py\n'
ICS_FOOTER = 'END:VCALENDAR'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Sessionize JSON input file')
    parser.add_argument('output', type=str, help='ICS output file')
    parser.add_argument('--utc', action='store_true', help='Use UTC time for timestamps')
    args = parser.parse_args()

    utc_postfix = 'Z' if args.utc else ''

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        sessions = data["schedule"]["sessions"]

        with open(args.output, 'w', encoding='utf-8') as calendar_file:
            calendar_file.write(ICS_HEADER)

            for session in sessions:
                # Begin event
                calendar_file.write('BEGIN:VEVENT\n')
                
                # Title/Summary
                calendar_file.write('SUMMARY:{0}\n'.format(session["title"]))

                # Location
                if session["roomName"]:
                    calendar_file.write('LOCATION:{0}\n'.format(session["roomName"]))

                # Categories
                categories = ''
                for category in session["categoryItemsEx"]:
                    if len(categories) > 0:
                        categories += ','
                    categories += str(category['name'])
                if categories:
                    calendar_file.write('CATEGORIES:{0}\n'.format(categories))

                # Description
                if session["description"]:
                    calendar_file.write('DESCRIPTION:{0}\n'.format(session["description"].replace(',', '\,').replace('\r\n','\n').replace('\n', '\\n')))
                    
                # Start and end time
                calendar_file.write('DTSTART:{0}{1}\n'.format(session["startsAt"].replace('-', '').replace(':', ''), utc_postfix))
                calendar_file.write('DTEND:{0}{1}\n'.format(session["endsAt"].replace('-', '').replace(':', ''), utc_postfix))
                
                # UID
                uid = str(uuid.uuid4())
                calendar_file.write('UID:{0}@{1}.org\n'.format(uid, uid[:4]))

                # End event
                calendar_file.write('END:VEVENT\n')

            calendar_file.write(ICS_FOOTER)