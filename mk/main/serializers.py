from .models import MyUser, SeniorStaff, Faculty, Contact
from rest_framework import serializers

class SeniorStaffSerializer(serializers.ModelSerializer):
    senior = serializers.CharField(source='get_extra_full_name')
    photo = serializers.CharField(source='get_only_photo_path')

    class Meta:
        model = SeniorStaff
        fields = ('senior', 'photo', 'description', )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ('email', 'password')

    def validate(self, attrs):
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': 'Пароль должен быть длинной более 8 символов'})
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'middle_name',
                  'email', 'gender', 'password')


class FacultiesSerializer(serializers.ModelSerializer):
    group_faculty=serializers.ListField(source = 'get_groups')

    class Meta:
        model = Faculty
        fields = ('name', 'group_faculty')

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'subject', 'body')