from authe.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions import ValidationError
from .utils import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id',)
        # fields = '__all__'

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/reset-password/' + uid + '/' + token

            # sending mail
            body = 'Click the Following Link to Reset Your Password ' + link
            data = {
                'subject' : 'Reset Your Password',
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)

            return attrs
        else:
            raise ValidationError("You are not a registered user!")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length= 255, style = {'input_type' : 'password'}, write_only = True)
    password2 = serializers.CharField(max_length= 255, style = {'input_type' : 'password'}, write_only = True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError("Passwords doesn't match!")

            id = smart_str(urlsafe_base64_decode(uid))        
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not Valid or Expired!')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not Valid or Expired!')
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            self.fail("bad token")