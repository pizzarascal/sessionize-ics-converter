# Sessionize to ICS Converter

A simple Python 3.X script for converting a Sessionize sessions JSON payload into a compatible iCalendar .ics file. Currently supports summary, description, location, categories, start date/time, and end date/time properties for calendar events.

## Usage

To create a calendar file from a Sessionize payload JSON file:

```shell
python ics_convert.py <input> <output>
```

Example:

```shell
python ics_convert.py data.json calendar.ics
```

By default the calendar file uses local timezone timestamps. To override this and use UTC timestamps instead, you can pass the optional parameter `--utc` to the command.

## License

This project is licensed under the [MIT License](LICENSE).