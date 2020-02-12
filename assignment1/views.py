import requests
from allauth.socialaccount.models import SocialToken
from django.shortcuts import render
from django.utils import timezone


def next_ten_events(request):
    user = request.user
    social_token = SocialToken.objects.filter(account__user=user, account__provider='google').first()

    response = requests.get(
        url='https://www.googleapis.com/calendar/v3/calendars/primary/events/',
        headers={'Authorization': 'Bearer ' + social_token.token},
        params={
            'timeMin': timezone.now().isoformat(),
            'maxResults': 10,
            'singleEvents': True,
            'orderBy': 'startTime',
        },
    )

    print(type(response.json()))

    return render(request, 'ten_events.html', {'calendar_data': response.json()})
