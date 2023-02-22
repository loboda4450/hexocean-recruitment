from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.reverse import reverse
from uuid import uuid4

from images.models import ImagesUser, Image


class ImagesUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImagesUser
        fields = ['username', 'password', 'email', 'groups']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        if ImagesUser.objects.filter(email=attrs.get("email")):
            raise serializers.ValidationError(f'There is an account connected with {attrs.get("email")} email address!')

        return attrs

    def create(self, validated_data):
        user = ImagesUser(username=validated_data.get('username'),
                          email=validated_data.get('email'))  # avoid raising DoesNotExist exception

        user.set_password(validated_data.get('password'))
        user.save()  # as I found in docs it's the best solution lol
        if validated_data.get('groups'):
            for group in validated_data.get('groups'):
                user.groups.add(group.id)

            user.save()

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']

    def create(self, validated_data):
        group = Group(name=validated_data.get('name'))
        group.save()

        if validated_data.get('permissions'):
            for perm in validated_data.get('permissions'):
                group.permissions.add(perm)

        for perm in ('add_image', "delete_image", 'view_image'):
            group.permissions.add(Permission.objects.get(codename=perm))

        group.save()
        return group


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['codename', 'name']

    def validate(self, attrs):
        if not attrs.get('codename').isdigit():
            raise serializers.ValidationError('Codename has to be integer type (e.g. 100, 300)')

        if Permission.objects.all().filter(codename=attrs.get("codename")):
            raise serializers.ValidationError(f'There is permission with {attrs.get("codename")} codename!')

        return attrs

    def create(self, validated_data):
        perm = Permission(name=validated_data.get('name'),
                          codename=validated_data.get('codename'),
                          content_type_id='7')

        perm.save()

        return perm


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pic_urls = serializers.SerializerMethodField(method_name='create_custom_url')

    # changed from imageid to prevent iterating over catalog
    # i know its hardly readable, but its pythonic shrug

    def create_custom_url(self, attrs):
        perms = [a.split('.')[1] for a in attrs.creator.get_all_permissions() if 'images' in a]
        urls = {perm: f"{reverse('image-pics', request=self.context['request'])}?imagename={attrs.image_name}" \
                      f"&size={perm}" for perm in perms if perm.isdigit() or perm == 'full'}

        if 'expiring_links' in perms:
            urls['expiring-binary'] = f"{reverse('image-generate-temp-url', request=self.context['request'])}" \
                                      f"/images/generate_temp_url?imagename={attrs.image_name}&timeout="

        return urls

    class Meta:
        model = Image
        fields = ['url', 'pic_urls', 'image_fullres', 'author']
        extra_kwargs = {
            'image_fullres': {'write_only': True},
            'pic_urls': {'read_only': True}
        }

    def validate(self, attrs):
        if (attrs.get('image_fullres')).content_type not in ('image/png', 'image/jpeg', 'image/jpg') or \
                (attrs.get('image_fullres')).image.format not in ('PNG', 'JPEG'):
            raise serializers.ValidationError(f'Wrong image format {attrs.get("image_fullres").image.format} '
                                              f'(should be JPG/PNG)')
        # double check just in case of content type injection

        return attrs

    def create(self, validated_data):
        img = validated_data.get('image_fullres')
        img.name = f'{uuid4()}.{img.image.format}'
        x = Image.objects.create(image_fullres=img,
                                 image_name=validated_data.get('image_fullres').name,
                                 binary=img.file.read(),
                                 creator=validated_data.get('author')
                                 )

        x.save()

        return x
