from myapp.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import User, Event, Ticket
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

# # User Registration
User = get_user_model()  # Get the custom user model

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'User')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=username, role=role)
        user.set_password(password)  # to create hash password
        user.save()

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)



# Event Management
class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'Admin':
            raise PermissionDenied({"error": "Only admins can create events"})  # Return 403 error
        serializer.save()




# Ticket Purchase
class TicketPurchaseView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is logged in

    def post(self, request, event_id):
        ####Allow only users (not admins) to purchase tickets
        if request.user.role.lower() == 'admin':
            raise PermissionDenied({"error": "Admins are not allowed to purchase tickets"})

        event = Event.objects.filter(id=event_id).first()
        if not event: 
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            quantity = int(request.data.get('quantity', 0))
        except ValueError:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
        
        ##### If quantity is negative or zero it gives an error
        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        ####To check the availability of tickets
        if event.tickets_sold + quantity > event.total_tickets:
            return Response({'error': 'Not enough tickets available'}, status=status.HTTP_400_BAD_REQUEST)

        ### Create ticket entry
        ticket = Ticket.objects.create(user=request.user, event=event, quantity=quantity)

        #### Update event tickets_sold
        event.tickets_sold += quantity
        event.save()

        return Response({'message': 'Ticket purchased successfully'}, status=status.HTTP_201_CREATED)
