from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt
from dateutil.parser import parse as parse_date


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def process_register(request):

    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    # redirect the user back to the form to fix the errors
        return redirect('/register')

    else:
        hash_pw = bcrypt.hashpw(
            request.POST['password_input'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name=request.POST['first_name_input'],
            last_name=request.POST['last_name_input'],
            email=request.POST['email_input'],
            password=hash_pw,
        )

        request.session['user_id'] = new_user.id

        return redirect('/dashboard')


def process_logout(request):
    request.session.clear()
    return redirect('/')


def process_login(request):
    user_list = User.objects.filter(email=request.POST['email_input'])
    if len(user_list) == 0:
        messages.error(request, "INVALID CREDENTIALS")
        return redirect("/login")
    logged_user = user_list[0]
    if bcrypt.checkpw(request.POST['password_input'].encode(), logged_user.password.encode()):
        # PASSWORD MATCHES
        request.session['user_id'] = logged_user.id
        return redirect("/dashboard")
    else:
        # PASSWORD DOES NOT MATCHES
        messages.error(request, "INVALID CREDENTIALS")
        return redirect("/login")


def dashboard(request):

    all_the_trips = Trip.objects.all()

    not_users_trips = []
    for trip in all_the_trips:
        if trip not in User.objects.get(id=request.session['user_id']).joined_trips.all():
            not_users_trips.append(trip)

    context = {
        'logged_user': User.objects.get(id=request.session['user_id']),
        'all_the_trips': Trip.objects.all(),
        'not_users_trips': not_users_trips,
    }
    return render(request, 'dashboard.html', context)


def trips_new(request):
    context = {
        'logged_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'new_trip_page.html', context)


def process_trip(request):

    print(request.POST)
    errors = Trip.objects.trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    # redirect the user back to the form to fix the errors
        return redirect('/trips/new')

    else:
        new_trip = Trip.objects.create(
            destination=request.POST['destination_input'],
            start_date=request.POST['trip_start_input'],
            end_date=request.POST['trip_end_input'],
            plan=request.POST['trip_plan_input'],
            creator=User.objects.get(id=request.session['user_id']))

        new_trip.trip_members.add(
            User.objects.get(id=request.session['user_id']))

        return redirect("/dashboard")


def trip_page(request, num):
    context = {
        'this_trip': Trip.objects.get(id=num),
        'logged_user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'trip_page.html', context)


def trip_join(request, num):
    this_trip = Trip.objects.get(id=num)
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip.trip_members.add(this_user)

    return redirect("/dashboard")


def trip_remove(request, num):
    this_trip = Trip.objects.get(id=num)
    this_trip.delete()
    return redirect("/dashboard")


def trip_update_page(request, num):
    context = {
        'this_trip': Trip.objects.get(id=num),
        'logged_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'trip_edit_page.html', context)


def update_trip(request, num):
    trip_to_edit = Trip.objects.get(id=num)
    print(trip_to_edit.start_date)
    errors = Trip.objects.trip_validator(request.POST)

    print(type(request.POST['destination_input']))

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    # redirect the user back to the form to fix the errors
        return redirect('/trips/new')

    else:
        trip_to_edit.destination = request.POST['destination_input']
        trip_to_edit.start_date = request.POST['trip_start_input']
        trip_to_edit.end_date = request.POST['trip_end_input']
        trip_to_edit.plan = request.POST['trip_plan_input']
        trip_to_edit.save()

        return redirect("/dashboard")


def trip_cancel(request, num):
    trip_to_cancel = Trip.objects.get(id=num)
    this_user = User.objects.get(id=request.session['user_id'])

    this_user.joined_trips.remove(trip_to_cancel)
    return redirect('/dashboard')
