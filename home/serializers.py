from rest_framework import serializers
from.models import User


 
class UserSerializer(serializers.ModelSerializer):
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',"Address", 'password')
        # fields = ['id', 'email', 'first_name',"Address",'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop("password",None)
        Instance = self.Meta.model(**validated_data)
        if password is not None:
            Instance.set_password(password)
        Instance.save()
        return Instance