from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label=_('პაროლი'))
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label=_('გაიმეორეთ პაროლი'))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'address', 'passport_id', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required': '{fieldname} აუცილებელია'.format(fieldname=self.fields[field].label)}
            self.fields[field].error_messages = {'blank': '{fieldname} აუცილებელია'.format(fieldname=self.fields[field].label)}

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 == password2:
            if len(password1) < 8:
                error_message = {'password': 'მინიმალური ასეობის რაოდენობა 8'}
                raise serializers.ValidationError(error_message)
        if password1 != password2:
            error_message = {'password': 'პაროლები ერთმანეთს არ ემთხვევა'}
            raise serializers.ValidationError(error_message)
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            passport_id=validated_data['passport_id'],
            address=validated_data['address']
        )
        password1 = self.validated_data.get('password1')
        user.set_password(password1)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('მეილი'), write_only=True)
    password = serializers.CharField(label=_('პაროლი'), write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(label=_('token'), read_only=True)

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': '{fieldname} აუცილებელია'.format(fieldname=field.label)}
            field.error_messages = {'blank': 'შეიყვანე {fieldname}'.format(fieldname=field.label)}

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                error_message = {'password':'პაროლი არასწორია'} if User.objects.filter(email=email) else {'email':'მაილი არასწორია'}
                raise serializers.ValidationError(error_message)

        data['user'] = user
        return data