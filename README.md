# Event Platform - SaaS Event Management System

Hey there! I'm a 19-year-old dev who built this cool SaaS Event Platform using Django and Django REST Framework. It's basically a system where people can create events, manage them, and let others enroll. Super useful for organizing meetups, conferences, or whatever events you can think of. Let me walk you through how to get it running and what it does.

## 🚀 Features

- **Multi-Tenant Architecture**: Each user belongs to a tenant, so you can have separate organizations
- **Event Management**: Create, edit, and view events with all the details
- **Ticket System**: Users can buy tickets for events (with unique UUIDs)
- **Team Support**: For events that need teams, like hackathons or sports
- **Sub-Events**: Break down big events into smaller parts
- **Announcements**: Keep everyone updated with event news
- **Frontend UI**: Simple web interface for creating and managing events
- **JWT Authentication**: Secure login with tokens

## 🛠️ Tech Stack

- **Backend**: Django 5.2.9 with Django REST Framework
- **Database**: SQLite (for dev, you can switch to PostgreSQL for prod)
- **Authentication**: JWT tokens with djangorestframework-simplejwt
- **Frontend**: Django templates with Bootstrap for styling
- **Python**: 3.11 (or whatever you're using)

## 📦 Installation & Setup

Alright, let's get this thing running. First, clone the repo or whatever:

```bash
git clone <your-repo-url>
cd event_platform
```

Make sure you have Python installed. Then:

1. **Create a virtual environment** (always a good idea):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

Boom! Your app is now running at `http://127.0.0.1:8000/`. Go check it out!

## 🎯 How to Use

### For Users:
- **Register/Login**: Create an account or log in
- **Home Page**: See all upcoming events
- **Create Event**: Click "Create Event" to add a new one
- **Edit Event**: If you created it, you can edit it
- **Enroll**: For events you didn't create, hit "Enroll" to get a ticket

### For Admins:
- Use the Django admin at `/admin/` to manage tenants, users, etc.
- All the REST APIs are available for programmatic access

## 📚 API Endpoints

Check out the full API docs in `API_DOCUMENTATION.md`. But basically:

- **Authentication**: `/api/token/` for login, `/api/token/refresh/` for refreshing tokens
- **Events**: `/api/events/` - CRUD operations
- **Tickets**: `/api/tickets/` - Manage your tickets
- **Teams**: `/api/teams/` - For team-based events
- And more!

## 🧪 Testing

I didn't write a ton of tests (hey, I'm 19 and busy), but you can run what's there:

```bash
python manage.py test
```

## 🚀 Deployment

For production, don't use the dev server. Use something like Gunicorn + Nginx. Also, switch to a real database like PostgreSQL. Environment variables for secrets, etc.

## 🤝 Contributing

If you wanna add features or fix bugs, fork it and submit a PR. I'm open to ideas!

## 📄 License

MIT License - do whatever you want with it.

---

Built with ❤️ by a 19-year-old who loves coding and events. Hit me up if you have questions!
