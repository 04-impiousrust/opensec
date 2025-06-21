# OpenSec Resources App

This project provides a simple Django application for collecting and ranking cybersecurity resources by upvotes.

Each resource on the list page now displays a small thumbnail preview fetched from [thum.io](https://thum.io/), making it easier to identify links at a glance.

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
