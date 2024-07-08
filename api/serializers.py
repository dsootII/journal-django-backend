from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Entry, Container

class EntrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Entry
    fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
  # entries = EntrySerializer(many=True)
  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'email']
    extra_kwargs = {'password': {'write_only': True}}
  
  def create(self, validated_data):
    print(validated_data)
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    
    return instance


class ContainerSerializer(serializers.ModelSerializer):
    entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ['id', 'name', 'entries', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        entries = Entry.objects.filter(container=instance)
        representation['entries'] = EntrySerializer(entries, many=True).data
        return representation