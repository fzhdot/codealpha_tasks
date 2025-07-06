from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'



class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import posts.signals  # adapter si ton app s’appelle autrement

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
