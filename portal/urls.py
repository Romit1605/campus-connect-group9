from django.urls import path, include
from .views import (
    HomeView,
    RegisterView,
    ProfileView,
    ProfileUpdateView,
    TicketCreateView,
    LostFoundCreateView,
    ReportListView,
    TicketDetailView,
    LostFoundDetailView,
    MyReportsView,
    TicketUpdateView,
    LostFoundUpdateView,
    UserHistoryView,
    AnnouncementListView,
    AboutView,
    ContactView,
    report_stats_api,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Authentication and profile
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),

    # Django built-in auth views
    path('accounts/', include('django.contrib.auth.urls')),

    # Submission forms
    path('tickets/new/', TicketCreateView.as_view(), name='ticket_create'),
    path('lost-found/new/', LostFoundCreateView.as_view(), name='lostfound_create'),

    # Reports and detail pages
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('lost-found/<int:pk>/', LostFoundDetailView.as_view(), name='lostfound_detail'),

    # My reports and edit pages
    path('my-reports/', MyReportsView.as_view(), name='my_reports'),
    path('tickets/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket_update'),
    path('lost-found/<int:pk>/edit/', LostFoundUpdateView.as_view(), name='lostfound_update'),

    # Sessions, cookies, and user history
    path('history/', UserHistoryView.as_view(), name='user_history'),

    # Announcements and public pages
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    # Simple API endpoint
    path('api/report-stats/', report_stats_api, name='report_stats_api'),
]