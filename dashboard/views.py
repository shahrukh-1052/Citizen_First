from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    IssueReport, EmergencyNumber, LostFoundItem, Event, 
    Feedback, EmergencyAlert, ChatMessage, Poll, PollOption, PollVote
)
from accounts.views import get_location_from_pincode

@login_required
def dashboard_view(request):
    from accounts.models import Profile
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'update_location' in request.POST:
        pincode = request.POST.get('pincode')
        if pincode:
            user_profile.pincode = pincode
            user_profile.save()
            messages.success(request, f"Pincode updated to {pincode}")
            return redirect('dashboard')

    full_name = user_profile.full_name or request.user.get_full_name() or request.user.username
    pincode_location = get_location_from_pincode(user_profile.pincode)
    
    context = {
        'full_name': full_name,
        'pincode_location': pincode_location,
        'local_body': user_profile.local_body,
        'profile': user_profile
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def about_us_view(request):
    return render(request, 'dashboard/aboutus.html')

@login_required
def contact_us_view(request):
    return render(request, 'dashboard/contactus.html')

@login_required
def emergency_view(request):
    numbers = EmergencyNumber.objects.all()
    # Group by category
    grouped_numbers = {}
    for num in numbers:
        if num.category not in grouped_numbers:
            grouped_numbers[num.category] = []
        grouped_numbers[num.category].append(num)
    
    return render(request, 'dashboard/emergency.html', {'grouped_numbers': grouped_numbers})

@login_required
def report_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        house_no = request.POST.get('house_no', '')
        street = request.POST.get('street', '')
        village = request.POST.get('village', '')
        area = request.POST.get('area', '')
        photo = request.FILES.get('photo')

        IssueReport.objects.create(
            user=request.user,
            category=category,
            description=description,
            house_no=house_no,
            street=street,
            village=village,
            area=area,
            photo=photo
        )
        messages.success(request, 'Issue reported successfully!')
        return redirect('report')

    my_reports = IssueReport.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/report.html', {'my_reports': my_reports})

@login_required
def events_view(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'dashboard/events.html', {'events': events})

@login_required
def alerts_view(request):
    alerts = EmergencyAlert.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'dashboard/alerts.html', {'alerts': alerts})

@login_required
def chat_view(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            message = request.POST.get('message')
            if message:
                ChatMessage.objects.create(user=request.user, message=message)
                return JsonResponse({'status': 'success'})
        # Handle Poll Vote
        poll_id = request.POST.get('poll_id')
        option_id = request.POST.get('option_id')
        if poll_id and option_id:
            try:
                poll = Poll.objects.get(id=poll_id)
                option = PollOption.objects.get(id=option_id)
                # Check if already voted
                if not PollVote.objects.filter(poll=poll, user=request.user).exists():
                    PollVote.objects.create(poll=poll, option=option, user=request.user)
                    messages.success(request, 'Vote recorded!')
                else:
                    messages.warning(request, 'You have already voted.')
            except:
                pass
            return redirect('chat')

    # Get recent messages
    messages_list = ChatMessage.objects.all().order_by('-timestamp')[:50]
    
    # Get active poll
    active_poll = Poll.objects.filter(is_active=True).last()
    poll_results = []
    if active_poll:
        total_votes = PollVote.objects.filter(poll=active_poll).count()
        for option in active_poll.options.all():
            votes = PollVote.objects.filter(poll=active_poll, option=option).count()
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            poll_results.append({
                'option': option,
                'votes': votes,
                'percentage': round(percentage, 1)
            })

    # Calculate last_id for polling (latest message ID)
    last_id = messages_list[0].id if messages_list else 0

    return render(request, 'dashboard/chat.html', {
        'chat_msgs': messages_list[::-1], # Show oldest first in UI
        'active_poll': active_poll,
        'poll_results': poll_results,
        'last_id': last_id
    })

@login_required
def get_chat_messages(request):
    last_id = request.GET.get('last_id', 0)
    new_messages = ChatMessage.objects.filter(id__gt=last_id).order_by('timestamp')
    data = [{
        'id': msg.id,
        'user': msg.user.username,
        'message': msg.message,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in new_messages]
    return JsonResponse({'messages': data})

@login_required
def lost_found_view(request):
    if request.method == 'POST':
        type_item = request.POST.get('type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        contact_info = request.POST.get('contact_info')
        date_lf = request.POST.get('date')
        image = request.FILES.get('image')

        LostFoundItem.objects.create(
            user=request.user,
            type=type_item,
            title=title,
            description=description,
            location=location,
            contact_info=contact_info,
            date_lost_found=date_lf,
            image=image
        )
        return redirect('lost_found')

    items = LostFoundItem.objects.all().order_by('-created_at')
    return render(request, 'dashboard/lost_found.html', {'items': items})

@login_required
def feedback_view(request):
    if request.method == 'POST':
        type_f = request.POST.get('type')
        message = request.POST.get('message')
        
        Feedback.objects.create(
            user=request.user,
            type=type_f,
            message=message
        )
        messages.success(request, 'Feedback submitted successfully!')
        return redirect('feedback')

    return render(request, 'dashboard/feedback.html')
