from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import RegistrationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from app.forms import LoginForm
from .forms import Level2Form, Level3Form, LoginForm
from . models import User
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from app.otpgeneration import OTPgen
import random
from django.views import View

error = 0
currentUser = ''
x = []


def home(request):
    return render(request, 'home.html')


class RegisterUser(View):
    def get(self, request):
        allImages = [
            'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
            'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
            'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
            'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
            'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
            'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
            'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
            'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
            'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
        ]
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form, 'images': allImages})

    def post(self, request):
        allImages = [
            'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
            'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
            'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
            'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
            'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
            'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
            'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
            'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
            'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
        ]
        msg = None
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            msg = "Make sure you have entered the Email ID in valid format and both the passwords match with each other"
            form = RegistrationForm()
            return render(request, 'register.html', {'form': form, 'msg': msg, 'images': allImages})


def send_error_mail(userId):
    user = User.objects.get(id=userId)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    print('Encoded ID is: ' + str(uid))
    link = 'http://127.0.0.1:8000/unblock/?uid=' + \
        uid + '/'
    print(link)
    body = "Dear User, Someone is trying to access your account, so your account has been blocked. Click on the link given below to unlock " + link
    data = {
        'subject': 'Account Blocked',
        'body': body,
        'to_email': str(user.email),
    }
    user.temp_blocked = True
    user.save()
    OTPgen.send_email(data)


class UnBlockUser(View):
    def get(self, request):
        uid = request.GET['uid']
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        user.temp_blocked = False
        user.save()
        return render(request, 'accountrecovered.html')


def login(request):
    allImages = [
        'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
        'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
        'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
        'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
        'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
        'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
        'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
        'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
        'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
    ]

    global error, currentUser, x
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email).exists()
            if(user is True):
                user = User.objects.get(email=email)
                if(user.temp_blocked is False):
                    if check_password(password, user.password):
                        x = allImages
                        random.shuffle(x)
                        form = Level2Form()
                        response = redirect('level2')
                        response.set_cookie('id', user.id)
                        return response
                    else:
                        msg = 'You have entered incorrect Email or password'
                        error += 1
                        if(error < 3):
                            return render(request, 'level1.html', {'form': form, 'msg': msg})
                        else:
                            send_error_mail(user.id)
                            return render(request, 'accessdenied.html')
                else:
                    return render(request, 'accessdenied.html')
            else:
                msg = 'You have entered incorrect Email or password'
                error += 1
                if(error < 3):
                    return render(request, 'level1.html', {'form': form, 'msg': msg})
                else:
                    send_error_mail(user.id)
                    return render(request, 'accessdenied.html')
        else:
            msg = 'Make sure you have entered the valid Email or Password'
    return render(request, 'level1.html', {'form': form, 'msg': msg})


def getCorrectSequence(newSequence, newImages):
    initialImages = [
        'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
        'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
        'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
        'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
        'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
        'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
        'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
        'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
        'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
    ]

    correctOne = ""
    for i in range(0, len(initialImages)):
        if(newImages[int(newSequence[0])-1] == initialImages[i]):
            correctOne += str(i+1)
        if(newImages[int(newSequence[1])-1] == initialImages[i]):
            correctOne += str(i+1)
        if(newImages[int(newSequence[2])-1] == initialImages[i]):
            correctOne += str(i+1)

    return correctOne


class Level2Auth(View):
    def get(self, request):
        global x
        allImages = [
            'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
            'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
            'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
            'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
            'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
            'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
            'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
            'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
            'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
        ]
        if(request.COOKIES.get('id')):
            x = allImages
            random.shuffle(x)
            form = Level2Form()
            return render(request, 'level2.html', {'form': form, 'images': x})
        else:
            return redirect('home')

    def post(self, request):
        allImages = [
            'https://cdn.britannica.com/s:800x450,c:crop/34/180334-138-4235A017/subordinate-meerkat-pack.jpg',
            'https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg',
            'http://wp.nathabblog.com/wp-content/uploads/2018/07/Panda_BradJosephs-4CROP_Web.jpg',
            'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
            'https://cdn.hswstatic.com/gif/animal-stereotype-orig.jpg',
            'https://i.natgeofe.com/n/f4d64d53-07ce-4933-a76e-1d405eec3473/giraffe_thumb_3x4.JPG',
            'https://www.airtransportanimal.com/wp-content/uploads/1970/01/panama-animal-transport-plane.jpg',
            'https://aldf.org/wp-content/uploads/2018/05/lamb-iStock-665494268-16x9-e1559777676675-1200x675.jpg',
            'https://www.awesomelycute.com/wp-content/uploads/2013/10/cute-baby-animals-2435.jpg',
        ]
        global error, x
        form = Level2Form(request.POST or None)
        msg = None
        if form.is_valid():
            userId = request.COOKIES['id']
            user = User.objects.get(id=userId)
            if(user.temp_blocked is False):
                p1 = form.cleaned_data.get('op1')
                p2 = form.cleaned_data.get('op2')
                p3 = form.cleaned_data.get('op3')
                if (int(p1) or int(p2) or int(p3) not in range(1, 9)):
                    print("YESS")
                    error += 1
                    if(error < 3):
                        x = allImages
                        random.shuffle(x)
                        form = Level2Form()
                        return redirect('level2')
                    else:
                        send_error_mail(user.id)
                        return render(request, 'accessdenied.html')
                pattern = str(p1) + str(p2) + str(p3)
                patternReceived = getCorrectSequence(pattern, x)
                if(patternReceived == str(user.pattern_order)):
                    otp_to_send = random.randint(100000, 999999)
                    body = "Dear User, Please use the following OTP " + \
                        str(otp_to_send) + " to login"
                    data = {
                        'subject': 'Login User',
                        'body': body,
                        'to_email': str(user.email),
                        'otp': str(otp_to_send),
                    }
                    print(otp_to_send)
                    user.otp = otp_to_send
                    user.save()
                    OTPgen.send_email(data)
                    return redirect('level3')
                else:
                    msg = 'You have entered incorrect Sequence'
                    error += 1
                    if(error < 3):
                        x = allImages
                        random.shuffle(x)
                        form = Level2Form()
                        return redirect('level2')
                    else:
                        send_error_mail(user.id)
                        return render(request, 'accessdenied.html')
            else:
                return render(request, 'accessdenied.html')
        else:
            msg = 'Make sure you have entered the valid Pattern Sequence'
            print(msg)
            error += 1
            if(error < 3):
                x = allImages
                random.shuffle(x)
                form = Level2Form()
                return redirect('level2')
            else:
                userId = request.COOKIES['id']
                user = User.objects.get(id=userId)
                send_error_mail(user.id)
                return render(request, 'accessdenied.html')


class Level3Auth(View):
    def get(self, request):
        if(request.COOKIES.get('id')):
            form = Level3Form()
            return render(request, 'level3.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request):
        global error
        form = Level3Form(request.POST or None)
        msg = None
        if form.is_valid():
            otp_entered = form.cleaned_data.get('otp')
            userId = request.COOKIES['id']
            user = User.objects.get(id=userId)
            if(user.temp_blocked is False):
                userOTP = user.otp
                if otp_entered == userOTP:
                    response = redirect('loggedin')
                    response.delete_cookie('id')
                    user.otp = None
                    user.save()
                    return response
                else:
                    msg = 'You have entered the Incorrect OTP'
                    error += 1
                    if(error < 3):
                        return render(request, 'level3.html', {'form': form, 'msg': msg})
                    else:
                        userId = request.COOKIES['id']
                        user = User.objects.get(id=userId)
                        send_error_mail(user.id)
                        return render(request, 'accessdenied.html')
            else:
                return render(request, 'accessdenied.html')
        else:
            msg = 'Make sure you have entered the valid OTP'
            error += 1
            if(error < 3):
                return redirect('level3')
            else:
                userId = request.COOKIES['id']
                user = User.objects.get(id=userId)
                send_error_mail(user.id)
                return render(request, 'accessdenied.html')


def resendOTP(request):
    msg = None
    userId = request.COOKIES['id']
    user = User.objects.get(id=userId)
    otp_to_send = random.randint(100000, 999999)
    body = "Dear User, Please use the following OTP " + \
        str(otp_to_send) + " to login"
    data = {
        'subject': 'Login User',
        'body': body,
        'to_email': str(user.email),
        'otp': str(otp_to_send),
    }
    print(otp_to_send)
    user.otp = otp_to_send
    user.save()
    OTPgen.send_email(data)
    return redirect('level3')


def loggedIn(request):
    return render(request, 'loggedin.html')


def logoutUser(request):
    logout(request)
    return redirect('home')
