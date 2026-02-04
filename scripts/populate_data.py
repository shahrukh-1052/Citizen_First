import os
import sys
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenFirst.settings')
django.setup()

from django.contrib.auth import get_user_model
from dashboard.models import (
    IssueReport, EmergencyNumber, LostFoundItem, Event, 
    Feedback, EmergencyAlert, ChatMessage, Poll, PollOption, PollVote
)

User = get_user_model()

def populate():
    print("Populating data...")

    # Create Users
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
    if _: admin_user.set_password('admin123'); admin_user.save()
    
    users = []
    for i in range(1, 6):
        u, _ = User.objects.get_or_create(username=f'citizen{i}', defaults={'email': f'citizen{i}@example.com'})
        if _: u.set_password('password123'); u.save()
        users.append(u)
    
    print(f"Created {len(users)} citizens and 1 admin.")

    # 1. Emergency Numbers
    emergencies = [
        ('Medical', 'City Hospital Ambulance', '102'),
        ('Medical', 'Apollo Emergency', '1066'),
        ('Security', 'Police Control Room', '100'),
        ('Security', 'Women Helpline', '1091'),
        ('Fire', 'Fire Station', '101'),
        ('Other', 'Disaster Management', '108'),
    ]
    
    EmergencyNumber.objects.all().delete()
    for cat, name, num in emergencies:
        cat_key = cat.upper() if cat.upper() in ['MEDICAL', 'SECURITY', 'FIRE'] else 'OTHER'
        EmergencyNumber.objects.create(category=cat_key, name=name, number=num)
    print("Populated Emergency Numbers.")

    # 2. Issue Reports
    issues_data = [
        ('TRASH', 'Garbage pile not collected for 3 days', '12/B', 'MG Road', 'Rampur', 'Market Area'),
        ('STREETLIGHT', 'Streetlight flickering and causing dark spot', '45', 'Sector 4', 'Rampur', 'Near Park'),
        ('WATER', 'Dirty water supply since morning', '88', 'Lane 2', 'Rampur', 'Housing Colony'),
        ('ROAD', 'Deep pothole in the middle of the road', '', 'Main Highway', 'Rampur', 'Near School'),
        ('ELECTRICITY', 'Frequent power cuts in evening', '101', 'Civil Lines', 'Rampur', 'Block A'),
    ]
    
    IssueReport.objects.all().delete()
    for cat, desc, house, street, vill, area in issues_data:
        IssueReport.objects.create(
            user=random.choice(users),
            category=cat,
            description=desc,
            house_no=house,
            street=street,
            village=vill,
            area=area,
            status=random.choice(['PENDING', 'IN_PROGRESS', 'RESOLVED'])
        )
    print("Populated Issue Reports.")

    # 3. Lost & Found
    lost_found_data = [
        ('LOST', 'Black Leather Wallet', 'Lost my wallet near the central bus stand. Contains ID cards.', 'Central Bus Stand'),
        ('FOUND', 'Car Keys (Toyota)', 'Found a set of car keys on a bench in the park.', 'City Park'),
        ('LOST', 'Golden Retriever Dog', 'Our dog Tommy went missing yesterday evening. Wearing a red collar.', 'Sector 7'),
        ('FOUND', 'Blue Umbrella', 'Left on a seat in the cinema hall.', 'PVR Cinema'),
    ]

    LostFoundItem.objects.all().delete()
    for type_dummy, title, desc, loc in lost_found_data:
        LostFoundItem.objects.create(
            user=random.choice(users),
            type=type_dummy,
            title=title,
            description=desc,
            date_lost_found=timezone.now().date() - timedelta(days=random.randint(0, 5)),
            location=loc,
            contact_info=f"987654321{random.randint(0,9)}"
        )
    print("Populated Lost & Found.")

    # 4. Events
    events_data = [
        ('Free Health Checkup Camp', 'General physician and specialized doctors available for free checkup.', 2, 'Community Center Hall'),
        ('Annual Cultural Fest', 'Celebration of local culture with dance, music, and food stalls.', 7, 'City Ground'),
        ('Blood Donation Drive', 'Join us to save lives. Refreshments provided for donors.', 14, 'Red Cross Building'),
        ('Town Hall Meeting', 'Discussing the new metro project with city officials.', 5, 'Municipal Corporation Office'),
    ]

    Event.objects.all().delete()
    for title, desc, days_ahead, loc in events_data:
        Event.objects.create(
            title=title,
            description=desc,
            date=timezone.now() + timedelta(days=days_ahead),
            location=loc
        )
    print("Populated Events.")

    # 5. Feedback
    feedbacks = [
        ('SUGGESTION', 'We need more dustbins in the market area.'),
        ('FEEDBACK', 'The new road in Sector 4 is very smooth. Great job!'),
        ('SUGGESTION', 'Please increase the frequency of water tankers in summer.'),
        ('FEEDBACK', 'Police patrolling at night has improved safety.'),
    ]

    Feedback.objects.all().delete()
    for type_choice, msg in feedbacks:
        Feedback.objects.create(
            user=random.choice(users),
            type=type_choice,
            message=msg
        )
    print("Populated Feedback.")

    # 6. Emergency Alerts
    alerts = [
        ('Heavy Rain Warning', 'Met department predicts heavy rainfall for next 24 hours. Stay indoors.', 'HIGH'),
        ('COVID-19 Vaccination Drive', 'Vaccination camp at City Hospital this Sunday.', 'LOW'),
        ('Road Closure Notice', 'Main bridge closed for maintenance on Sunday.', 'MEDIUM'),
    ]

    EmergencyAlert.objects.all().delete()
    for title, msg, severity in alerts:
        EmergencyAlert.objects.create(
            title=title,
            message=msg,
            severity=severity
        )
    print("Populated Emergency Alerts.")

    # 7. Chat Messages
    chat_msgs = [
        ("Has anyone noticed the new park lights?", "Yes, they look great at night!"),
        ("When is the next community meet?", "I think it's next Saturday."),
        ("Please drive slowly near the school.", "Agreed, safety first."),
        ("Found a set of keys near the gate.", "Please post in Lost & Found tab."),
    ]
    
    ChatMessage.objects.all().delete()
    for q, a in chat_msgs:
        # Question
        ChatMessage.objects.create(
            user=random.choice(users),
            message=q,
            timestamp=timezone.now() - timedelta(minutes=random.randint(10, 60))
        )
        # Answer
        ChatMessage.objects.create(
            user=random.choice(users),
            message=a,
            timestamp=timezone.now() - timedelta(minutes=random.randint(1, 9))
        )
    print("Populated Chat Messages.")

    # 7. Polls
    poll = Poll.objects.create(
        question="What should be the priority for next month's budget?",
        created_by=admin_user
    )
    options = ['Road Repair', 'Park Renovation', 'Streetlights', 'Water Supply']
    for opt_text in options:
        PollOption.objects.create(poll=poll, text=opt_text)
    
    # Random votes
    for u in users:
        PollVote.objects.create(
            poll=poll,
            option=random.choice(poll.options.all()),
            user=u
        )
    print("Populated Polls.")

    print("Data population complete!")

if __name__ == '__main__':
    populate()
