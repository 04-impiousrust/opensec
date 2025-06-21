# OpenSec Resources App

This project provides a simple Django application for collecting and ranking cybersecurity resources by upvotes.

Each resource on the list page now displays a small thumbnail preview fetched from
[microlink.io](https://microlink.io/). The screenshots are requested with a `colorScheme=dark`
so thumbnails match the rest of the interface.

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
