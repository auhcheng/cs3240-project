# Node

## How to use

Features:
- Weather: shows the weather based on your location geocoded by ip
- Profile: change your preferred name by clicking "Hello, <name>"
- To-do list: mark todos as complete/incomplete, overdue tasks are colored red, sorted by due date, click on tasks to edit them
- Notes: write notes, archive them, or delete them; search by keyword
- Calendar: add and edit events

To run the server locally, first run the following:

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open http://localhost:8000/

Also should be currently deployed at https://project-101-node.herokuapp.com/



## Requirements

### Sprint 2

- Create login and user account system

### Sprint 3

- Figure out how to get the app to interact with other apps and systems
- Make sure Dashboard can display that information and update itself
- Get the dashboard to keep track of the weather

### Sprint 4

- Add a scheduler (schedules one day of events)
- No calendar yet
- Add a note creation, storage, and display system

### Sprint 5

- Add a calendar for multi-day scheduling
- Add a notification system

### Sprint 6

- Add email notification and display system
- Add toggle and other features to notification system

### Final Polish

- Finish customizing the notification system
- Make scheduling and organizing easy
- Make the app easy to use in general

## Citations
Much of the calendar was borrowed from https://github.com/huiwenhw/django-calendar, accessed April 15

Weather was built with the help of https://www.youtube.com/watch?v=qCQGV7F7CUc, https://github.com/PrettyPrinted/weather_app_django, accessed Feb 17

Datetime picker in Bootstrap uses Tempus Dominus at https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html, accessed April 15

MIT License

Copyright 2020 Node.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
