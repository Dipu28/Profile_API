from rest_framework import serializers

from profile_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView """
    name = serializers.CharField(max_length=10)


# User profile
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user prfile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password')
        # We want password only when we are creating a new user to the system
        # We don't want the user to Retrieve the password hash(Due to security reason)
        extra_kwargs = {
            'password':{
                'write_only':True,
                # Styling(Dot Dot Dot for password)
                'style':{'input_type':'password'}
            }
        }
        # Overiding the create function, by default the model serializer allows you to create simple objects in the Database
        # It uses default cerate function of the object Manager to create the object .
        # We want to overide thisn functionalty for this particular serializer, so that it uses the "create user function" instead of the create function
        # The main reason is to create the password as hash not the clear password

    def create(self, validated_data):
        """ Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, isinstance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            isinstance.set_password(password)
        return super().update(isinstance,validated_data)



class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id','user_profile','status_text','created_on')
        extra_kwargs = {'user_profile': {'read_only':True}}
