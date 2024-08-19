/mailroom/
│
├── /mailer/
│   ├── /models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── /views/
│   │   ├── __init__.py
│   │   └── user_view.py
│   │
│   ├── /controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   │
│   ├── /config/
│   │   └── config.py
│   │
│   ├── /migrations/
│   └── __init__.py
│
├───── run.py
│
├── /scripts/
│   └── setup_db.py
│
└── /docs/
    └── api_documentation.md
    └── setup.md

*Creating Virtual Environment and Installing Libraries*
```$ python -m venv venv```
```$ source venv/bin/activate```
```$ pip install Flask Flask-SQLAlchemy Flask-Migrate```

*Registering Flask App*
```$ set FLASK_APP=run.py```

*DB Migration*
```$ flask db init```
```$ flask db migrate -m "Initial migration."```
```$ flask db upgrade```

*Running Flask Application*
```$env:FLASK_APP = "run.py"```
```flask run```
