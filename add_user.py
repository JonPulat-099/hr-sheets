from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.filter(username='admin001').exists() or \
    User.objects.create_superuser('admin001', 'admin@gmail.com', 'admin001')