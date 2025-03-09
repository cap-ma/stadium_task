from django.shortcuts import render
from .models import User
from django.db.models import Q
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import FootballField, Booking
from .serializers import FootballFieldSerializer, BookingSerializer
from django.utils.decorators import method_decorator 
import math
from .permissions import IsFieldOwnerOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from datetime import datetime
from rest_framework.exceptions import ParseError

class UserRegistrationView(APIView):
    
    @swagger_auto_schema(
        tags=["Authentication"],
        request_body=UserSerializer,  # Explicitly define request body
        responses={201: UserSerializer()}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):

    @swagger_auto_schema(
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': "invalide username or password"}, status=401)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Authentication"],
    )
    def post(self, request):
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail' : "Logged out succesfully"})


class FootballFieldListAPIView(generics.ListAPIView):
    queryset = FootballField.objects.all().order_by('-id')
    serializer_class = FootballFieldSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @method_decorator(swagger_auto_schema(tags=["stadium"]))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FootballFieldDetailAPIView(generics.RetrieveAPIView):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @method_decorator(swagger_auto_schema(tags=["stadium"]))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_serializer_context(self):
        """Pass request context to serializer for full image URLs."""
        return {'request': self.request}

class FootballFieldCreateAPIView(generics.CreateAPIView):
    serializer_class = FootballFieldSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @method_decorator(swagger_auto_schema(tags=["stadium"],   security=[{'Token': []}] ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class FootballFieldUpdateAPIView(generics.UpdateAPIView):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # @method_decorator(swagger_auto_schema(tags=["stadium"]))
    # def put(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["stadium"],
        request_body=FootballFieldSerializer  # Explicitly define the request body
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class FootballFieldDeleteAPIView(generics.DestroyAPIView):
    queryset = FootballField.objects.all()
    serializer_class = FootballFieldSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    
    @method_decorator(swagger_auto_schema(tags=["stadium"]))
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AvailableFootballFieldsAPIView(generics.ListAPIView):
    serializer_class = FootballFieldSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        booking_date = self.request.query_params.get('booking_date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        user_lat = self.request.query_params.get('lat')
        user_lon = self.request.query_params.get('lon')

       
        def validate_time(time_str):
            if not time_str:
                return None
            try:
                return datetime.strptime(time_str.strip(), "%H:%M").time()
            except ValueError:
                raise ParseError(f"Invalid time format: '{time_str}'. Must be in 'HH:MM' format.")

        start_time = validate_time(start_time)
        end_time = validate_time(end_time)
        
        fields = FootballField.objects.all()
        
        if booking_date and start_time and end_time:
            from .models import Booking
            booked_fields = Booking.objects.filter(
                booking_date=booking_date
            ).filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
            ).values_list('field_id', flat=True)
            fields = fields.exclude(id__in=booked_fields)
        
        if user_lat and user_lon:
            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
                for field in fields:
                    field.distance = math.sqrt(
                        (field.latitude - user_lat) ** 2 + (field.longitude - user_lon) ** 2
                    )
                fields = sorted(fields, key=lambda f: f.distance)
            except ValueError:
                pass
        
        return fields
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('booking_date', openapi.IN_QUERY, description="Booking Date (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('start_time', openapi.IN_QUERY, description="Start Time (HH:MM)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_time', openapi.IN_QUERY, description="End Time (HH:MM)", type=openapi.TYPE_STRING, ),
            openapi.Parameter('lat', openapi.IN_QUERY, description="User Latitude", type=openapi.TYPE_NUMBER),
            openapi.Parameter('lon', openapi.IN_QUERY, description="User Longitude", type=openapi.TYPE_NUMBER),
        ],
        tags=["stadium"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(swagger_auto_schema(tags=["booking"]))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(swagger_auto_schema(tags=["booking"]))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @method_decorator(swagger_auto_schema(tags=["booking"]))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
    def perform_create(self, serializer):
        field = serializer.validated_data['field']
        booking_date = serializer.validated_data['booking_date']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        overlapping_bookings = Booking.objects.filter(
            field=field,
            booking_date=booking_date,
        ).filter(
            start_time__lt=end_time,  
            end_time__gt=start_time,  
        )

        if overlapping_bookings.exists():
            raise ValidationError("This stadium is already booked for the selected time.")

        serializer.save(user=self.request.user)

class BookingDeleteAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFieldOwnerOrAdmin]
    
    @method_decorator(swagger_auto_schema(tags=["booking"]))
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class BookingUpdateAPIView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(swagger_auto_schema(tags=["booking"]))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)




