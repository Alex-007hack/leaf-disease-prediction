from django.shortcuts import render,redirect
from .models import Discussion, Feedback, Users
from django.contrib import messages
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from tensorflow.keras.models import load_model
import os

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        return render(request,"index.html",{'current_user':current_user,'user':user})
    return render(request,"index.html")
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        phoneno=request.POST['phone']
        emailexists=Users.objects.filter(EmailID=email)
        if emailexists:
            messages.error(request,"Email ID already registered")
        elif password!=cpassword:
            messages.error(request,"Password doesnot match")
        else:
            Users.objects.create(Name=name,EmailID=email,Password=password,PhoneNo=phoneno)
            return redirect('/')
    return render(request,"register.html")
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=Users.objects.filter(EmailID=email,Password=password)
        if user:
            request.session['EmailID']=email
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,"login.html")

def deleteUploadedImage(session_key,extension):
    file_name = f"{session_key}{extension}" 
    file_path = os.path.join('static/assets/uploads/', file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

def logout(request):
    deleteUploadedImage(request.session['EmailID'],request.session['uploadedFileExtension'])
    del request.session['EmailID']
    return redirect('/')
def profile(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        return render(request,"profile.html",{'current_user':current_user,'user':user})
def updateprofile(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        if request.method=='POST':
            name=request.POST['name']
            password=request.POST['password']
            cpassword=request.POST['cpassword']
            phoneno=request.POST['phone']
            if password!=cpassword:
                messages.error(request,"Password doesnot match")
            else:
                user.Name=name
                user.Password=password
                user.PhoneNo=phoneno
                user.save()
                return redirect('profile')
        return render(request,"updateprofile.html",{'current_user':current_user,'user':user})
    

def handleUploadedFile(request, file, current_user):
    file_name, file_extension = os.path.splitext(file.name)
    new_file_name = f"{current_user}{file_extension}"
    extension = f"{file_extension}"
    request.session['uploadedFileExtension'] = extension
    destination_path = os.path.join('static/assets/uploads/', new_file_name)
    with open(destination_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def prediction(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        def preprocess_image(image_path, target_size=(225, 225)):
            img = load_img(image_path, target_size=target_size)
            x = img_to_array(img)
            x = x.astype('float32') / 255.
            x = np.expand_dims(x, axis=0)
            return x

        # Load the model from the .h5 file
        model = load_model('static/assets/h5/final5.h5')
        if request.method=='POST':
            uploadedImage = request.FILES['image']
            if uploadedImage:
                handleUploadedFile(request, uploadedImage, current_user)
            
            ext = request.session['uploadedFileExtension']
            x = preprocess_image("static/assets/uploads/"+current_user+ext)

            # Make predictions
            predictions = model.predict(x)
            # Assuming you have a dictionary that maps class indices to class labels
            class_labels = {
                0: 'healthy',
                1: 'powdery',
                2: "rust"
            # Add more class indices and labels as needed
            }

            # Make predictions
            predictions = model.predict(x)

            # Get the predicted class index
            predicted_class_index = np.argmax(predictions[0])

            # Get the corresponding class label
            predicted_class_label = class_labels[predicted_class_index]

            messages.success(request,"Predicted Disease:")
            messages.success(request, predicted_class_label)
            return render(request,"prediction.html",{'current_user':current_user,'user':user,'predict':predicted_class_label})
        return render(request,"prediction.html",{'current_user':current_user,'user':user})
    else:
        return render(request,"prediction.html")
def powderyprequations(request):
    return render(request,"powderyprequation.html")
def rustprequations(request):
    return render(request,"rustprecaution.html")
def feedback(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        if request.method=='POST':
            name=request.POST['name']
            condition=request.POST['condition']
            accurancy=request.POST['accurancy']
            Feedback.objects.create(Name=name,Condition=condition,Accurancy=accurancy)
            return redirect('/')
        return render(request,"feedbackform.html",{'current_user':current_user,'user':user})
    return render(request,"feedbackform.html")
def communityform(request):
    if 'EmailID' in request.session:
        current_user=request.session['EmailID']
        user=Users.objects.get(EmailID=current_user)
        if request.method=='POST':
            name=request.POST['name']
            experience=request.POST['experience']
            Discussion.objects.create(Name=name,Experience=experience)
            return redirect('/')
        return render(request,"communityform.html",{'current_user':current_user,'user':user})
    else:
        return render(request,"communityform.html")
def discussionboard(request):
    exp=Discussion.objects.all()
    return render(request,"discussionboard.html",{'exp':exp})

def sendalert(request):
    email=request.POST['email']
    message=request.POST['message']
    print('email', email)
    print('message', message)

    subject = 'Message About Leaf Disease'
    # message = ' This is a smaple alert message from leaf prediction '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]   
    send_mail( subject, message, email_from, recipient_list ) 
    return redirect('/')