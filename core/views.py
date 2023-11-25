from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random 

# Create your views here.
@login_required(login_url='signin')
def index (request):
    user_name = request.user.username
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = Post.objects.all()

    #getting posts for the accounts user is following
    account_follows = []
    their_post = []

    follow = Follow.objects.filter(follower = user_name)
    
    for pple in follow:
        account_follows.append(user_name)
        account_follows.append(pple.being_followed)
    
    for user in account_follows:
        posts = Post.objects.filter(user=user)
        their_post.append(posts)
    
    post_list = list(chain(*their_post))   

    #user you can follow
    all_account_being_followed = []
    followedby_loggedinaccount = []
    all_users = Follow.objects.all()

    for uzer in all_users:
        uzer_name = uzer.being_followed #getting names for all users being followed in the platform
        all_account_being_followed.append(uzer_name)
    for name in follow:
        followed_name = name.being_followed
        followedby_loggedinaccount.append(followed_name)
    
    listt = [x for x in all_account_being_followed if x not in followedby_loggedinaccount ]
    owner = [user_name]
    suggestions = [x for x in listt if x not in owner] #remove the name for logged in user
    suggestions = list(set(suggestions)) #remove duplicates from the list
    
    profile_suggested_user = [] #Get profile for the suggested users

    for name in suggestions:
        user = User.objects.get(username = name)
        profile = Profile.objects.get(user=user)
        profile_suggested_user.append(profile)

    collection = {
        'user_profile':user_profile,
        'post':post_list,
        'user_object':user_object,
        'suggested_user':profile_suggested_user[:5]
    }
    return render(request,"index.html",collection)

def signin (request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)

            return redirect('index')
        else:
            messages.info(request,'Invalid credation')

            return redirect('signin')

    else:
        return render(request,'signin.html')
    
def signup (request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

         
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Email already taken!')
                return redirect('signup')
            
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Username already taken!')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
        
                #create profile for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user = user_model.id)
                new_profile.save()

                return redirect('settings')
            
        else:
            messages.info(request, 'Password do not match!')

            return redirect('signup')

    return render(request,"signup.html")

@login_required(login_url='signin')
def profile (request):
    user_name = request.user.username
    user = User.objects.get(username = user_name)
    user_profile = Profile.objects.get(user=user)
    post = Post.objects.filter(user=user_name)
    len_of_post = len(post)
    account_being_followed = Follow.objects.filter(follower=user_name)
    account_following = Follow.objects.filter(being_followed=user_name)
    
    
    collection = {
        'no_of_post':len_of_post,
        'user_profile':user_profile,
        'posts':post,
        'account_being_followed':account_being_followed,
        'account_following':account_following
        
    }
    return render(request,"profile.html",collection)

@login_required(login_url='signin')
def profile_poster(request):
    if_profile_is_for_accountowner = request.user.username
    user_name = request.GET.get('user')
    user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=user)
    post = Post.objects.filter(user=user_name)
    len_of_posts = len(post)
    follow_unfollow = Follow.objects.filter(follower=if_profile_is_for_accountowner,being_followed=user_name).first()
    followers = Follow.objects.filter(being_followed=user_name)
    account_following = Follow.objects.filter(follower=user_name)
    
    dic = {
        'len_of_posts':len_of_posts,
        'profile':profile,
        'posts':post,
        'follow':followers,
        'account_following':account_following,
        'name':if_profile_is_for_accountowner,
        'follow_unfollow':follow_unfollow
        
    }

    return render(request,'poster_profile.html',dic)

@login_required(login_url='signin')
def likes(request):
    name = request.user.username
    id = request.GET.get('post_id')
    


    post = Post.objects.get(id = id)
    like_filter  = Likes.objects.filter(username=name,post_id=id).first()

    if like_filter == None:
        like = Likes.objects.create(username =user,post_id=id)
        like.save()
        post.no_of_like = post.no_of_like +1
        post.save()

        return redirect('index')

    else:
        post.no_of_like = post.no_of_like - 1
        post.save()
        like_filter  = Likes.objects.get(username=user,post_id=id)
        like_filter.delete()

       
        
        return redirect('index')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.user.username
        being_followed = request.POST['being_followed']
        userobject_followed = User.objects.get(username=being_followed)
        profileobject_followed = Profile.objects.get(user=userobject_followed)

        if Follow.objects.filter(follower=follower,being_followed=being_followed).first() == None:
            new_object = Follow.objects.create(follower=follower,being_followed=being_followed,follower_pro=profileobject_followed)
            new_object.save()

            return redirect(f'/profile/profile?user={being_followed}')

        else:
            folo = Follow.objects.get(follower=follower,being_followed=being_followed)
            folo.delete()

            return redirect(f'/profile/profile?user={being_followed}')

    else:
        return redirect(f'/profile/profile?user={being_followed}')

@login_required(login_url='signin')
def upload(request):
    #upload posts
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST['Caption']
        user_object = User.objects.get(username=user)
        user_profile = Profile.objects.get(user=user_object)

        print('user_pro')
        
        my_post = Post.objects.create(user=user,image=image,user_pro=user_profile,caption=caption,)
        print("reacted post")
        my_post.save()

        return redirect('index')
    else:
        return redirect('index')
    
    return render(request,'index.html')

@login_required(login_url='signin')
def comment(request):

    if request.method == 'POST':

        commenter = request.POST['commenter']
        post_id = request.POST['post_id']
        comment = request.POST['comment']
        

        comment_model = Comment.objects.create(commenter=commenter,post_id=post_id,comment=comment)
        comment_model.save()
        return redirect('index')
    
    else:
        return redirect('index')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.pro_image
            bio = request.POST['bio']

            user_profile.pro_image = image
            user_profile.bio = bio
            user_profile.save()

        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']

            user_profile.pro_image = image
            user_profile.bio = bio

            user_profile.save()
            
    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def logout (request):
    auth.logout(request)

    return redirect('signin')

@login_required(login_url='signin')
def post(request):
    #posts for a spcific profile only
    user_name = request.GET.get('poster')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = Post.objects.filter(user=user_name)

      
    collection = {
        'user_profile':user_profile,
        'post':post,
        'user_object':user_object,
    }
    return render(request,'post.html',collection)

@login_required(login_url='signin')
def delete_post(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('index')