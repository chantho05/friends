from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Friend

# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):

    results = User.objects.register_valdiation(request.POST)

    if results[0]:

        request.session['user_id'] = results[1].id
        print "******* You registered yo! ******"
        return redirect('/friends')
    else:
        for err in results[1]:
            messages.error(request, err)
        return redirect('/')

def login(request):
    results = User.objects.login_validation(request.POST)
    
    if results[0]:
        request.session['user_id'] = results[1].id 
        print "******* logged in yo! ******"
        return redirect(friends)
    else:
        for err in results[1]:
            messages.error(request, err)
        return redirect('/')

def logout(request):
    request.session.flush()
    print "++++++++ You logged out ++++++++++"
    return redirect('/')

#Home Page
def friends(request):
    context = {
        "username": User.objects.get(id=request.session['user_id']).name,
        "email": User.objects.get(id=request.session['user_id']).email,
        "many": User.objects.get(id=request.session['user_id']),
    }
    # friends = user.objects.all()
    # all_users = User.objects.all()

    # user_list = []
    # for u in all_users:
    #     if u not in friends and u != user:
    #         user_list.append(u)

    # friends_list = []
    # for f in friends:
    #     if f != user:
    #         friends_list.append(f)

    # context = {
    #     'User': user, 
    #     'friends': friends_list,
    #     'users': user_list,
    # }
    return render(request , "friends.html", context)

def add(request):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    Friend.objects.create(from_person=user, to_person=friend)
    Friend.objects.create(from_person=friend, to_person=user)
    user.save()

    return redirect('/friends')

def remove(request):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    Friend.objects.filter(from_person=user, to_person= friend).delete()
    Friend.objects.filter(from_person=friend, to_person=user).delete()

    return redirect('/friends')

def user(request):
    context = {
        "username": User.objects.get(id=request.session['user_id']).name,
        "email": User.objects.get(id=request.session['user_id']).email,
    }
    # user = User.objects.get(id=id)
    # context = {
    #     'User': user,
    # }
    return render(request, "user.html", context)

def otheruser(request):
    context = {
        "username": User.objects.get(id=request.session['user_id']).name,
        "email": User.objects.get(id=request.session['user_id']).email,
    }

    return render(request, "otheruser.html", context)