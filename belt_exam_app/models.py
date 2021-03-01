from django.db import models
import re
from datetime import date, datetime
from dateutil.parser import parse as parse_date


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        # name lengths
        if len(postData['first_name_input']) < 2:
            errors["first_name_input"] = "First name should be at least 2 characters."
        if len(postData['last_name_input']) < 2:
            errors["last_name_input"] = "Last name should be at least 2 characters."
        # email pattern
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_input']):
            errors['email_input'] = "Invalid email address!"
        # CHECK IF EMAIL ALREADY EXISTS WITH THE DB
        user_list = User.objects.filter(email=postData['email_input'])
        if len(user_list) > 0:
            errors['email_duplicate'] = "Email aleady exists, try logging in with this email."
        # password length
        if len(postData['password_input']) < 8:
            errors["password_input"] = "Password should be at least 8 characters long."
        # passwords matching
        if postData['password_input'] != postData['confirm_password_input']:
            errors['match_password'] = "Passwords do not match."

        return errors


class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}

        # Required
        if len(postData['destination_input']) < 1:
            errors['destination_input'] = "Destination name is required."
        if len(postData['trip_plan_input']) < 1:
            errors['trip_plan_input'] = "Trip plan is required."

        # Destinations and plans must be at least 3 characters logging
        if len(postData['destination_input']) < 3:
            errors['destination_input'] = "Destination name must be longer than 3 characters."
        if len(postData['trip_plan_input']) < 3:
            errors['trip_plan_input'] = "Trip plan must be longer than 3 characters."

        # Dates
        start_date = postData['trip_start_input']
        end_date = postData['trip_end_input']

        if start_date:
            start_date = parse_date(start_date).date()
            if start_date < date.today():
                errors['trip_start_date_in_past'] = "Trip start date must be in the future"
        else:
            errors['no_start_date'] = "Start date is required"

        if end_date:
            end_date = parse_date(end_date).date()
            if end_date < date.today():
                errors['trip_end_date_in_past'] = "Trip end date must be in the future"
        else:
            errors['no_end_date'] = "End date is required"

        if start_date and end_date:
            if start_date > end_date:
                errors['trip_end_date_invalid'] = "You cant time Travel!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # trips created
    # trips attending

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    trip_members = models.ManyToManyField(User, related_name='joined_trips')
    creator = models.ForeignKey(
        User, related_name='created_trips', on_delete=models.CASCADE)

    objects = TripManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
