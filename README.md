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

## 3-Clause BSD License

Copyright 2020 Node
  
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
