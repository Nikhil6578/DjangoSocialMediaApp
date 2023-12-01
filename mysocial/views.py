from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .form import (SignUpForm, UserLoginForm)
from django.shortcuts import render, redirect
from .models import UserProfile, FriendRequest


def home(request):
    return render(request, "home.html")


def signup_or_update(request):
    is_update = request.user.is_authenticated

    if is_update:
        data = get_object_or_404(UserProfile, user_id=request.user.id)
        initial_instance = {
            'phone_number': data.phone_number,
            'gender': data.gender,
            'dob': data.dob,
            'address': data.address,
            'user_image': data.user_image
        }
    else:
        initial_instance = {}

    if request.method == 'POST':
        form = SignUpForm(
            request.POST,
            request.FILES,
            initial=initial_instance,
            exclude=['username', 'email', 'password1', 'password2'] if
            is_update else []
        )

        if form.is_valid():
            user_image = request.FILES.get('user_image')
            phone_number = form.cleaned_data['phone_number']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']
            address = form.cleaned_data['address']

            if is_update:
                if user_image:
                    data.user_image = user_image
                data.phone_number = phone_number
                data.gender = gender
                data.dob = dob
                data.address = address
                data.save()
            else:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                user = User.objects.create_user(username=username, email=email,
                                                password=password)
                UserProfile.objects.create(
                    user=user,
                    user_image=user_image,
                    phone_number=phone_number,
                    gender=gender,
                    dob=dob,
                    address=address
                )

            return redirect('/mysocial/userdetail/' if is_update
                            else '/mysocial/login/')
    else:
        form = SignUpForm(
            initial=initial_instance,
            exclude=['username', 'email', 'password1', 'password2'] if
            is_update else []
        )

    context = {'form': form, 'is_update': is_update}
    return render(request, 'sign.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username,
                                password=password
                                )
            if user:
                login(request, user)
                return redirect('/posts/user_post/')

            else:
                error_message = ("Invalid username or password. "
                                 "Please try again.")
                return render(request, "login.html",
                              {'error_message': error_message})

    else:
        form = UserLoginForm()

    return render(request, "login.html", {'form': form})


@login_required
def user_detail(request):
    # Use get_object_or_404 to retrieve the user's profile, or
    # return 404 response if not found
    data = get_object_or_404(UserProfile, user_id=request.user.id)

    return render(request, "userdetail.html",
                  {'data': data}
                  )


@login_required
def friend_suggestion(request):
    # search bar text
    query = request.GET.get('q')

    user_profile = request.user.userprofile
    other_user_profiles = UserProfile.objects.exclude(
        user=request.user)

    if query:
        other_user_profiles = (other_user_profiles.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query))
        )

    friend_requests = FriendRequest.objects.filter(
        Q(to_user=user_profile) |
        Q(from_user=user_profile)
    ).select_related('from_user', 'to_user')

    friend_requests_data = friend_requests.values(
        'from_user__user__username', 'to_user__user__username', 'status'
    )

    sent_list = []
    receive_list = []

    for item in friend_requests_data:
        if item['status'] == 'pending':
            if item['from_user__user__username'] == user_profile.user.username:
                sent_list.append(item['to_user__user__username'])
            elif item['to_user__user__username'] == user_profile.user.username:
                receive_list.append(item['from_user__user__username'])

    accepted_user_profiles = UserProfile.objects.filter(
        Q(sent_requests__status='accepted',
          sent_requests__to_user=user_profile) |
        Q(received_requests__status='accepted',
          received_requests__from_user=user_profile)
    ).distinct().exclude(user=request.user)

    context = {
        'other_user_profiles': other_user_profiles,
        'sent_list': sent_list,
        'receive_list': receive_list,
        'friend_list': accepted_user_profiles,
    }

    return render(request, 'friend_suggestion.html', context)


@login_required
def send_or_cancel_friend_request(request, user_id):
    # Get the sender (from_user) and receiver (to_user) UserProfile objects
    from_user = get_object_or_404(UserProfile, user_id=request.user.id)
    to_user = get_object_or_404(UserProfile, id=user_id)

    # Check if a pending friend request already exists
    existing_request = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user,
        status='pending'
    )

    if existing_request:
        # Delete the friend request
        existing_request.delete()
    else:
        # Create a new friend request if one does not exist
        friend_request = FriendRequest(
            from_user=from_user,
            to_user=to_user,
            status='pending'
        )
        friend_request.save()

    # Redirect to the friend_suggestion view after processing the request
    return redirect('/mysocial/friend_suggestion/')


@login_required
def friend_request_list(request):
    user_profile = request.user.userprofile
    received_requests = FriendRequest.objects.filter(
        to_user=user_profile,
        status='pending'
    )

    return render(request, "friend_request_list.html",
                  {'received_requests': received_requests}
                  )


@login_required
def manage_receive_friend_request(request, request_id, action):
    # Get the FriendRequest object
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user.userprofile,
        status='pending'
    )

    # Process the action based on the parameter
    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.delete()

    # Redirect to the friend suggestion page after accepting
    # or rejecting the friend request
    return redirect('/mysocial/friend_suggestion/')


@login_required
def friends_list(request):
    user_profile = get_object_or_404(
        UserProfile.objects.select_related('user'), user=request.user)

    # Fetch accepted friend requests where the logged-in user is either
    # the sender or receiver
    accepted_friend_requests = (FriendRequest.objects.filter(
        (Q(from_user=user_profile) | Q(to_user=user_profile)) &
        Q(status='accepted')
    ).select_related('from_user__user', 'to_user__user')
                                .order_by('-created_at'))

    friends = []
    for friend_request in accepted_friend_requests:
        if friend_request.from_user != user_profile:
            friend_user = friend_request.from_user.user
        else:
            friend_user = friend_request.to_user.user
        friend = {
            'username': friend_user.username,
            'friendship_at': friend_request.created_at,
            'id': friend_user.id,
            'url': friend_user.userprofile.user_image.url,
        }
        friends.append(friend)

    return render(request, "friend_list.html",
                  {'friend': friends})


@login_required
def user_friend_delete(request, request_id):
    user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
    friend_profile = get_object_or_404(UserProfile, user_id=request_id)

    # Check if there is an accepted FriendRequest between the user
    # and the friend
    friend_request = FriendRequest.objects.filter(
        (Q(from_user=user_profile, to_user=friend_profile) |
         Q(from_user=friend_profile, to_user=user_profile))
        &
        Q(status='accepted')
    ).first()

    if friend_request:
        # Remove the friend
        friend_request.delete()

    return redirect('/mysocial/friendslist/')


@login_required
def logout_view(request):
    # This will log out the user and terminate the session
    logout(request)

    return redirect('/mysocial/login/')
