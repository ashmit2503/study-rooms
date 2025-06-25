#!/bin/sh

echo "Running database migrations..."
python manage.py migrate

echo "Creating media directories..."
mkdir -p media/profile_pics

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
python manage.py shell -c "
from django.contrib.auth.models import User
from base.models import UserProfile
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    profile, created = UserProfile.objects.get_or_create(user=user)
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "Starting Django development server..."
exec "$@"
