from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        if basic := Group.objects.get_or_create(name='Basic'):
            basic[0].permissions.add(
                Permission.objects.get(codename='200'),
            )

        if premium := Group.objects.get_or_create(name='Premium'):
            premium[0].permissions.add(
                Permission.objects.get(codename='200'),
                Permission.objects.get(codename='400'),
            )
        if enterprise := Group.objects.get_or_create(name='Enterprise'):
            enterprise[0].permissions.add(
                Permission.objects.get(codename='200'),
                Permission.objects.get(codename='400'),
                Permission.objects.get(codename='full'),
            )
