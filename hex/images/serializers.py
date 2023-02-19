from django.contrib.auth.models import Group, Permission
from images.models import ImagesUser, Image
from rest_framework import serializers
from uuid import uuid4


class ImagesUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImagesUser
        fields = ['url', 'username', 'password', 'email', 'groups']

    def validate(self, attrs):
        if ImagesUser.objects.filter(email=attrs.get("email")):
            raise serializers.ValidationError(f'There is an account connected with {attrs.get("email")} email address!')

        return attrs

    def create(self, validated_data):
        user = ImagesUser(username=validated_data.get('username'),
                          email=validated_data.get('email'))  # avoid raising DoesNotExist exception

        user.set_password(validated_data.get('password'))
        user.save()  # as I found in docs it's the best solution lol
        user.groups.add(validated_data.get('groups')[0].id)
        user.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']

    # def validate(self, attrs):
    #     if Group.objects.all().filter(name=attrs.get('name'))


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['url', 'codename', 'name']

    def validate(self, attrs):
        if not attrs.get('codename').isdigit():
            raise serializers.ValidationError('Codename has to be integer type (e.g. 100, 300)')

        if Permission.objects.all().filter(codename=attrs.get("codename")):
            raise serializers.ValidationError(f'There is permission with {attrs.get("codename")} codename!')

        return attrs

    def create(self, validated_data):
        perm = Permission(name=validated_data.get('name'),
                          codename=validated_data.get('codename'),
                          content_type_id='1')

        perm.save()

        return perm


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = ['url', 'image_fullres', 'creator', 'author']

    def validate(self, attrs):
        if (attrs.get('image_fullres')).content_type not in ('image/png', 'image/jpeg', 'image/jpg') or \
                (attrs.get('image_fullres')).image.format not in ('PNG', 'JPEG'):
            raise serializers.ValidationError(f'Wrong image format {attrs.get("image_fullres").image.format} '
                                              f'(should be JPG/PNG)')
        # double check just in case content type injection

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
