from django.urls import path
from .views import (
    dashboard_view, about_us_view, contact_us_view,
    emergency_view, report_view, events_view,
    alerts_view, chat_view, lost_found_view,
    feedback_view, get_chat_messages
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('about-us/', about_us_view, name='about_us'),
    path('contact-us/', contact_us_view, name='contact_us'),
    path('emergency/', emergency_view, name='emergency'),
    path('report/', report_view, name='report'),
    path('events/', events_view, name='events'),
    path('alerts/', alerts_view, name='alerts'),
    path('chat/', chat_view, name='chat'),
    path('chat/get/', get_chat_messages, name='get_chat_messages'),
    path('lost-found/', lost_found_view, name='lost_found'),
    path('feedback/', feedback_view, name='feedback'),
]
