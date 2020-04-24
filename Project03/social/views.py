from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from . import models
import datetime

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)

        posts = models.Post.objects.order_by('-timestamp').all()
        amount = 1
        if 'post' not in request.session:
            request.session['post'] = 1
        else:
            amount = int(request.session['post'])
        posts = posts[:amount]
        for post in posts:
            if user_info in post.likes.all():
                post.has_liked = True
            else:
                post.has_liked = False

        context = { 'user_info' : user_info
                  , 'posts' : posts }
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """
    if request.user.is_authenticated:
        form = None
        msg = ''
        info_msg = ''

        if request.method == 'POST':
            operation = request.POST['operation']
            if operation == 'password':
                password = request.POST['password']
                password1 = request.POST['new_password1']
                password2 = request.POST['new_password2']

                if password1 != password2:
                    msg = 'Two password entries are inconsistent.'
                else:
                    user = authenticate(username=request.user.username, password=password)
                    if user is None:
                        msg = 'your password is incorrect, try again.'
                    else:
                        user.password = make_password(password1)
                        user.save()
                        login(request, user)
                        msg = 'your password has been changed.'
            else:
                user_info = models.UserInfo.objects.get(user=request.user)

                user_info.employment = request.POST['employment']
                user_info.location = request.POST['location']
                user_info.birthday = request.POST['birthday']

                user_info.interests.clear()
                interests = str(request.POST['interests'])
                interests_list = interests.split(' ')
                for i in interests_list:
                    if i != '':
                        r = models.Interest()
                        r.label = i
                        r.save()
                        user_info.interests.add(r)
                user_info.save()
                info_msg = 'your info has been updated.'

        user_info = models.UserInfo.objects.get(user=request.user)
        context = { 'user_info' : user_info,
                    'form' : form,
                    'msg' : msg,
                    'info_msg' : info_msg}
        return render(request,'account.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        all_people = []
        friends = user_info.friends.all()
        for u in models.UserInfo.objects.all():
            if u not in friends and u != user_info:
                all_people.append(u)

        amount = 1
        if 'ppl' not in request.session:
            request.session['ppl'] = 1
        else:
            amount = int(request.session['ppl'])
        all_people = all_people[:amount]

        friend_requests = models.FriendRequest.objects.filter(to_user=user_info).all()

        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'friend_requests' : friend_requests }

        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
    ----------
      request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model

    Returns
    -------
         out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('postID')
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        postID = postIDReq[5:]
        post = models.Post.objects.get(id=int(postID))

        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.get(user=request.user)
            post.likes.add(user_info)

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
    ----------
      request : (HttpRequest) - should contain json data with attribute postContent, a string of content

    Returns
    -------
         out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    if postContent is not None:
        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.get(user=request.user)
            post = models.Post()
            post.owner = user_info
            post.content = postContent
            post.timestamp = datetime.datetime.now()
            post.save()

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
    ----------
      request : (HttpRequest) - should be an empty POST

    Returns
    -------
         out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of posts dispalyed

        amount = int(request.session['post'])
        amount += 1
        request.session['post'] = amount

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
    ----------
      request : (HttpRequest) - should be an empty POST

    Returns
    -------
         out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of people dispalyed

        amount = int(request.session['ppl'])
        amount += 1
        request.session['ppl'] = amount

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
    ----------
      request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username

    Returns
    -------
         out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    frID = request.POST.get('frID')
    if frID is not None:
        # remove 'fr-' from frID
        username = frID[3:]

        if request.user.is_authenticated:
            from_user = models.UserInfo.objects.get(user=request.user)
            user = models.User.objects.get(username=username)
            to_user = models.UserInfo.objects.get(user=user)

            fr = models.FriendRequest.objects.filter(from_user=from_user, to_user=to_user).all()
            if len(fr) == 0:
                fr = models.FriendRequest()
                fr.from_user = from_user
                fr.to_user = to_user
                fr.save()

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
    ----------
      request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)

    Returns
    -------
         out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('decision')
    if data is not None:
        adID = request.POST.get('adID')
        username = adID[2:]
        user = models.User.objects.get(username=username)
        user_info = models.UserInfo.objects.get(user=user)

        if request.user.is_authenticated:
            my_info = models.UserInfo.objects.get(user=request.user)
            if data == 'Accept':
                user_info.friends.add(my_info)
                my_info.friends.add(user_info)
                user_info.save()
                my_info.save()

            fr = models.FriendRequest.objects.filter(from_user=user_info, to_user=my_info).all()
            fr.delete()

            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('accept-decline-view called without decision in POST')
