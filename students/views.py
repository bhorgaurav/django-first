import re
import os

from random import randint
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException
from django.shortcuts import render
from students.models import VerificationCodes, StudentRecord

regex_phone = r'^[0-9]{10}$'
regex_pin = r'^[0-9]{1,6}$'

#  Can be added to global config later
TWILIO_ACCOUNT_SID = 'ACc2b7d002d365d4e5d0f90bd2f1a5006c'
TWILIO_AUTH_TOKEN = '2b320151aa1686bc62fb22f787ddac3a'
TWILIO_PHONE_NUMBER = '+12012796636'

def register(request):
    context = {
        'action': reverse('students:submit'),
    }
    return render(request, 'students/register.html', context)

def verify(request):
    mobile_number = request.POST.get('mobile_number', '')
    if re.match(regex_phone, mobile_number):
        # To separate registration and view info verification process. 1 = registration. 2 = view info.
        type_flag = request.POST.get('type_flag')

        # Generate random pin
        pin = randint(100000, 999999);
        # print(pin)
        # Save to database
        q = VerificationCodes(mobile_number=mobile_number, pin=pin, type_flag=type_flag)
        q.save();

        # Send SMS via twilio
        sms = send_SMS(mobile_number, pin)
        if sms == 1:
            return HttpResponse(type_flag)
        else:
            return HttpResponse(0)
    else:
        return HttpResponse(0)

def info_get(request):
    context = {
        'action': reverse('students:info_show'),
    }
    return render(request, 'students/info_get.html', context)

def success(request):
    return render(request, 'students/success.html')

def submit(request):
    pin = request.POST.get('input_pin', '')
    mobile_number = request.POST.get('mobile_number', '')
    name = request.POST.get('input_name', '')
    class_name = request.POST.get('input_class', '')
    type_flag = request.POST.get('type_flag', '')

    # Can add better validation. Probably using django forms.
    if re.match(regex_pin, pin) and re.match(regex_phone, mobile_number) and name and class_name and type_flag:
        try:
            # If the mobile and code exist.
            v = VerificationCodes.objects.get(mobile_number=mobile_number, pin=pin, type_flag=type_flag)

            # Avoid duplicates
            sr = StudentRecord.objects.filter(mobile_number=mobile_number).first()
            if not sr:
                sr = StudentRecord.objects.create(mobile_number=mobile_number, name=name)
                sr.save()

            # Avoid duplicates
            sc = sr.studentclasses_set.filter(class_name=class_name).first()
            if not sc:
                sc = sr.studentclasses_set.create(class_name=class_name)
            sc.save()

            response = { "url": reverse('students:success')}
            v.delete()
            return JsonResponse(response)
        except VerificationCodes.DoesNotExist:
            return HttpResponse(0)
        except StudentRecord.DoesNotExist:
            return HttpResponse(0)
    else:
        return HttpResponse(0)

def info_show(request):
    pin = request.POST.get('input_pin', '')
    mobile_number = request.POST.get('mobile_number', '')
    type_flag = request.POST.get('type_flag', '')
    if re.match(regex_pin, pin) and re.match(regex_phone, mobile_number):
        try:
            # If the mobile and code exist. Check and delete.
            v = VerificationCodes.objects.get(mobile_number=mobile_number, pin=pin, type_flag=type_flag)
            sr = StudentRecord.objects.filter(mobile_number=mobile_number).first()
            if sr:        
                context = {
                    "record": sr,
                }
                v.delete()
                return render(request, 'students/info_show.html', context)
            else:
                return HttpResponse(0)    
        except VerificationCodes.DoesNotExist:
            return HttpResponse(0)
        except StudentRecord.DoesNotExist:
            return HttpResponse(2)
    else:
        return HttpResponse(3)        

def send_SMS(mobile_number, pin):
    try:
        client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(from_=TWILIO_PHONE_NUMBER, to=mobile_number, body='Your PIN for verification is ' + str(pin))
        return 1
    except TwilioRestException:
        return 0