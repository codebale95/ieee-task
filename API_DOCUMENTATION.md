# API Documentation - Event Platform

Yo! This is the API docs for the Event Platform I built. I'm 19 and just learning this stuff, so if something's wrong, sorry! This is a REST API built with Django REST Framework. All endpoints require authentication except login/register.

## 🔐 Authentication

First things first - you gotta log in to use most of this.

### Login
**POST** `/api/token/`

Send your username and password to get JWT tokens.

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### Refresh Token
**POST** `/api/token/refresh/`

Get a new access token when the old one expires.

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_access_token"
}
```

## 👥 User Management

### List Users
**GET** `/api/users/`

Get all users in your tenant.

**Headers:** `Authorization: Bearer <access_token>`

**Response:** Array of user objects

### Create User
**POST** `/api/users/`

Create a new user.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

## 🏢 Tenants

### List Tenants
**GET** `/api/tenants/`

Get all tenants (admin only).

**Headers:** `Authorization: Bearer <access_token>`

## 📅 Events

### List Events
**GET** `/api/events/`

Get all events in your tenant.

**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Awesome Event",
    "description": "This event is awesome",
    "date": "2026-01-15T10:00:00Z",
    "location": "Conference Hall",
    "capacity": 100,
    "created_by": 1,
    "tenant": 1
  }
]
```

### Create Event
**POST** `/api/events/`

Create a new event.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "title": "My Event",
  "description": "Description here",
  "date": "2026-01-15T10:00:00Z",
  "location": "Some Place",
  "capacity": 50
}
```

### Get Event Details
**GET** `/api/events/{id}/`

Get a specific event.

### Update Event
**PUT/PATCH** `/api/events/{id}/`

Update an event (only if you created it).

### Delete Event
**DELETE** `/api/events/{id}/`

Delete an event (only if you created it).

## 🎫 Tickets

### List Your Tickets
**GET** `/api/tickets/`

Get all your tickets.

**Headers:** `Authorization: Bearer <access_token>`

### Purchase Ticket
**POST** `/api/tickets/purchase/`

Buy a ticket for an event.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "event_id": 1,
  "sub_event_id": null,
  "team_id": null
}
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "event": 1,
  "sub_event": null,
  "team": null,
  "uuid": "unique-ticket-uuid",
  "created_at": "2026-01-07T12:00:00Z"
}
```

## 👥 Teams

### List Teams
**GET** `/api/teams/`

Get all teams in your tenant's events.

### Create Team
**POST** `/api/teams/`

Create a new team for an event.

### Join Team
**POST** `/api/teams/{id}/join_team/`

Join a specific team.

**Headers:** `Authorization: Bearer <access_token>`

## 📢 Announcements

### List Announcements
**GET** `/api/announcements/`

Get all announcements for your tenant's events.

### Create Announcement
**POST** `/api/announcements/`

Create a new announcement.

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "title": "Important Update",
  "content": "The event time has changed",
  "event": 1
}
```

## 🚨 Error Responses

Most errors will look like this:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

Or for validation errors:

```json
{
  "field_name": ["This field is required."]
}
```

## 💡 Tips

- All dates are in ISO format (like "2026-01-15T10:00:00Z")
- Use the access token in the Authorization header: `Bearer <token>`
- Refresh your token before it expires (usually 5-15 minutes)
- Most endpoints filter by your tenant automatically
- For team events, make sure to join a team before buying a ticket

That's pretty much it! If you need help, check the Django REST Framework docs or ask me. I'm still learning this stuff too! 😄
