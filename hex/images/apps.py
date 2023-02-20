from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):  # preparing built-in groups
        from django.contrib.auth.models import Group, Permission
        if basic := Group.objects.get_or_create(name='Basic'):
            basic[0].permissions.add(
                Permission.objects.get(codename='200'),
                Permission.objects.get(codename='add_image'),
                Permission.objects.get(codename='delete_image'),
                Permission.objects.get(codename='view_image')
            )

        if premium := Group.objects.get_or_create(name='Premium'):
            premium[0].permissions.add(
                Permission.objects.get(codename='200'),
                Permission.objects.get(codename='400'),
                Permission.objects.get(codename='add_image'),
                Permission.objects.get(codename='delete_image'),
                Permission.objects.get(codename='view_image')
            )

        if enterprise := Group.objects.get_or_create(name='Enterprise'):
            enterprise[0].permissions.add(
                Permission.objects.get(codename='200'),
                Permission.objects.get(codename='400'),
                Permission.objects.get(codename='full'),
                Permission.objects.get(codename='add_image'),
                Permission.objects.get(codename='delete_image'),
                Permission.objects.get(codename='view_image')
            )
