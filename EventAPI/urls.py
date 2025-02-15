from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views import RegisterView, EventListCreateView, TicketPurchaseView

urlpatterns = [
    path('admin/', admin.site.urls),
    # User Registration
    path('api/register/', RegisterView.as_view(), name='register'),

    # Authentication (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/events/', EventListCreateView.as_view(), name='event-list-create'),
    path('api/events/<int:event_id>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
]
