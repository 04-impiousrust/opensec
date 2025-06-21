# OpenSec Resources App

This project provides a simple Django application for collecting and ranking cybersecurity resources by upvotes.

Each resource on the list page displays a small thumbnail preview generated
server side. Thumbnails are fetched from [thum.io](https://www.thum.io/). The
image is inverted in CSS so the preview fits the application's dark
theme.

## Setup

1. Ensure Django is installed (`pip install django`).
2. Run migrations:

```bash
python manage.py migrate
```

3. Start the server:

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` to see the resources list.
