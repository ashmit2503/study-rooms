# StudyRooms 📚

A Django-based web application for creating and managing virtual study rooms where users can collaborate, discuss topics, and share knowledge.

## Features ✨

- **User Authentication**: Registration, login, and profile management
- **Study Rooms**: Create, update, and delete study rooms with topics
- **Real-time Messaging**: Post and view messages within study rooms
- **Topic-based Organization**: Categorize rooms by study topics
- **User Profiles**: Extended profiles with bio, location, website, and more
- **Search Functionality**: Find rooms and topics easily

## Tech Stack 🛠️

- **Backend**: Django 4.0+
- **Database**: PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker & Docker Compose
- **Package Management**: Poetry

## Quick Start 🚀

### Prerequisites

- Docker & Docker Compose

### Docker Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd study-rooms
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   
   Open your browser and navigate to `http://localhost:8000`

4. **Stop and cleanup**
   ```bash
   docker-compose down -v
   ```

## Project Structure 📁

```
study-rooms/
├── base/                   # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   └── templates/         # HTML templates
├── studyrooms/            # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── templates/             # Global templates
├── contrib/               # Configuration samples
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile.dev         # Development Docker image
├── pyproject.toml         # Poetry dependencies
├── Makefile              # Development commands
└── README.md             # This file
```

## Usage Guide 📖

### Creating a Study Room

1. Register an account or log in
2. Click "Create Room" from the home page
3. Fill in room details:
   - Room name
   - Topic (new or existing)
   - Description
4. Click "Create Room"

### Joining Discussions

1. Browse available rooms on the home page
2. Use the search bar to find specific topics or rooms
3. Click on a room to join the discussion
4. Post messages to participate

### Managing Your Profile

1. Click on your username in the navigation
2. Select "Edit Profile" to update your information
3. Add bio, location, website, and birth date
4. Save changes

**Happy Studying! 🎓**