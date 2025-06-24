# OpenSec Resources App

This project provides a simple Django application for collecting and ranking cybersecurity resources by upvotes.

Each resource on the list page displays a small thumbnail preview generated
server side. Thumbnails are fetched from [thum.io](https://www.thum.io/). The
image is inverted in CSS so the preview fits the application's dark
theme.

## Security

The application enables several security-related HTTP headers via
Django's `SecurityMiddleware`. These include a referrer policy of
`same-origin` and the `X-Content-Type-Options` header to prevent MIME
type sniffing. Session and CSRF cookies are also marked as secure when
the environment provides HTTPS.

## Setup


1. Ensure Django is installed (`pip install django`).
2. Run migrations:

```bash
python manage.py migrate
```

3. Create a superuser:

```bash
python manage.py createsuperuser
```

4. Start the server:

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` to see the resources list and `http://localhost:8000/manage/` for the admin panel.
