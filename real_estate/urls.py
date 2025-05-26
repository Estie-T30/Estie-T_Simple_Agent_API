from django.urls import path
from .views import AllHouseListView, AppointmentReadOnlyView, HouseImageCreateView, UserCreateView, UserListView, HouseCreateView, PublicHouseListView, HouseDetailView, AppointmentListCreateView, AppointmentDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('houses/', PublicHouseListView.as_view(), name='house-list'),
    path('houses/all/', AllHouseListView.as_view(), name='all-house-list'),
    path('houses/create/', HouseCreateView.as_view(), name='house-create'),
    path('houses/image/', HouseImageCreateView.as_view(), name='house-image-create'),
    path('houses/<int:pk>/', HouseDetailView.as_view(), name='house-details'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentReadOnlyView.as_view(), name='appointment-readonly'),
    path('appointments/manage/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-manage-for-appointment-owner')
]