import datetime
import logging
import os
import time
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Create the log file if it doesn't exist
        if not os.path.exists("requests.log"):
            with open("requests.log", "w"):
                pass

    def __call__(self, request):
        # Open the log file in append mode
        with open("requests.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - User: {request.user} - Path: {request.path}\n")

        # Continue processing the request
        response = self.get_response(request)

        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = datetime.strptime("21:00", "%H:%M").time()  # 9 PM
        end_time = datetime.strptime("06:00", "%H:%M").time()    # 6 AM

        # Restrict access if the current time is not between 9 PM and 6 AM
        if not (current_time >= start_time or current_time <= end_time):
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # Dictionary to track requests by IP

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = time.time()

        if request.method == 'POST':
            if ip not in self.requests:
                self.requests[ip] = []

            # Remove outdated entries (older than 1 minute)
            self.requests[ip] = [timestamp for timestamp in self.requests[ip] if now - timestamp < 60]

            # Check if user has exceeded 5 messages in the last minute
            if len(self.requests[ip]) >= 5:
                return HttpResponseForbidden("Too many messages sent. Please wait before sending more.")

            # Record the current request
            self.requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in and has the required role (admin or moderator)
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to access this resource.")

        user_role = request.user.role  # Assuming the user has a `role` attribute

        # Check if the user is either an admin or moderator
        if user_role not in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to access this resource.")

        response = self.get_response(request)
        return response
