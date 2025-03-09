from rest_framework import serializers
from .models import User, FootballField, Booking, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class ImageSerializer(serializers.ModelSerializer):
    
    path = serializers.SerializerMethodField()  


    class Meta:
        model = Image
        fields = ['name', 'path']
    
    def get_path(self, obj):
        """Return full image URL."""
        request = self.context.get('request')
        if obj.path:
            return request.build_absolute_uri(obj.path.url) if request else obj.path.url
        return None

class FootballFieldSerializer(serializers.ModelSerializer):
   
    images = ImageSerializer(many=True, required=False, source="image_set")

    class Meta:
        model = FootballField
        fields = [
            'id',
            'owner',
            'name',
            'address',
            'contact',
            'hourly_rate',
            'latitude',
            'longitude',
            'images'
        ]
        read_only_fields = ['owner']

    def create(self, validated_data):

        request = self.context.get('request')
       
        images_data = request.FILES.getlist('images')
      
        print(images_data, 'this is datasa')
       
        football_field = FootballField.objects.create(**validated_data)
        print()
        for image in images_data:
            # Check if the image data is a dict (normal case)
            if isinstance(image, dict):
                Image.objects.create(football_field=football_field, **image)
            else:
                # Otherwise, it's likely an InMemoryUploadedFile
                # Use image.name for the name and assign the file to 'path'
                Image.objects.create(football_field=football_field, name=image.name, path=image)
            print('image createdddd--')
        return football_field

class BookingSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ['user', 'created_at']

