from django.contrib import admin
from .models import (
    IssueReport, EmergencyNumber, LostFoundItem, Event, 
    Feedback, EmergencyAlert, ChatMessage, Poll, PollOption, PollVote
)

admin.site.register(IssueReport)
admin.site.register(EmergencyNumber)
admin.site.register(LostFoundItem)
admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(EmergencyAlert)
admin.site.register(ChatMessage)

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [PollOptionInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(PollVote)
