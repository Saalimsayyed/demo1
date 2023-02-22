from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, UserImage


def signup(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        if otp == '00000':
            name = request.POST.get('name')
            user = User.objects.create_user(username=mobile, password=otp, first_name=name)
            return HttpResponse('User created successfully!')
        else:
            return HttpResponse('Invalid OTP')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        user = authenticate(request, username=mobile, password=otp)
        if user is not None:
            login(request, user)
            return HttpResponse('Welcome ' + user.first_name)
        else:
            return HttpResponse('Invalid mobile or OTP')
    else:
        return render(request, 'signin.html')



@login_required
def home(request):
    images = [
        {'url': 'http://getdrawings.com/get-icon#one-icon-3.png', 'name': 'One'},
        {'url': 'http://getdrawings.com/get-icon#free-shirt-icon-9.png', 'name': 'Two'},
        {'url': 'http://getdrawings.com/get-icon#serial-number-icon-19.png', 'name': 'Three'},
        {'url': 'http://getdrawings.com/get-icon#serial-number-icon-18.png', 'name': 'Four'},
        {'url': 'http://getdrawings.com/get-icon#number-one-icon-17.png', 'name': 'Five'},
    ]
    current_image_index = request.session.get('current_image_index', 0)
    if current_image_index >= len(images):
        return HttpResponse(request.user.first_name + ', you have rated all the images. Thank You!')
    current_image = images[current_image_index]
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reject':
            message = request.user.first_name + ', you have rejected image ' + current_image['name']
        else:
            message = request.user.first_name + ', you have selected image ' + current_image['name']
        request.session['current_image_index'] = current_image_index + 1
    else:
        message = None
    return render(request, 'home.html', {'image': current_image, 'message': message})


def swipe(request):
    if request.method == 'POST':
        user = request.user
        image_id = request.POST.get('image_id')
        direction = request.POST.get('direction')
        image = User.objects.get(id=image_id)

        # save user's swipe to the database
        # ...

        if direction == 'left':
            message = f'{user.username}, you have rejected image {image.name}'
        else:
            message = f'{user.username}, you have selected image {image.name}'

        return JsonResponse({'message': message})


@login_required
def history(request):
    user_images = UserImage.objects.filter(user=request.user)
    context = {'user_images': user_images}
    return render(request, 'history.html', context)