from django.shortcuts import render, redirect, reverse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from predictor.forms import BreastCancerForm, DiabetesForm, HeartDiseaseForm, SignUpForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    return render(request, 'home.html', {})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


# Now we dive into signup() function. It gets user data from HTTP POST request which is handled by SignUpForm, save user to database.

# Then we use authenticate() function and login() function from django.contrib.auth to log the user in.

# If the process is successful, redirect to homepage, otherwise, return to signup.html template.

def heart(request):
    """ 
    18:39:18 09 Oct, 2023 by Irvene Kwambana
    Reading the training data set. 
    """
    df = pd.read_csv('static/Heart_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1:]

    """ 
    18:39:18 09 Oct, 2023 by Irvene Kwambana
    Reading data from the user. 
    """

    value = ''

    if request.method == 'POST':

        age = float(request.POST['age'])
        sex = float(request.POST['sex'])
        cp = float(request.POST['cp'])
        trestbps = float(request.POST['trestbps'])
        chol = float(request.POST['chol'])
        fbs = float(request.POST['fbs'])
        restecg = float(request.POST['restecg'])
        thalach = float(request.POST['thalach'])
        exang = float(request.POST['exang'])
        oldpeak = float(request.POST['oldpeak'])
        slope = float(request.POST['slope'])
        ca = float(request.POST['ca'])
        thal = float(request.POST['thal'])

        user_data = np.array(
            (age,
             sex,
             cp,
             trestbps,
             chol,
             fbs,
             restecg,
             thalach,
             exang,
             oldpeak,
             slope,
             ca,
             thal)
        ).reshape(1, 13)

        rf = RandomForestClassifier(
            n_estimators=16,
            criterion='entropy',
            max_depth=9
        )

        rf.fit(np.nan_to_num(X), Y)
        rf.score(np.nan_to_num(X), Y)
        predictions = rf.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"

    return render(request,
                  'heart.html',
                  {
                      'context': value,
                      'title': 'Heart Disease Prediction',
                      'active': 'btn btn-success peach-gradient text-white',
                      'heart': True,
                      'form': HeartDiseaseForm(),
                  })


def diabetes(request):
    """ 
    20:13:20 09 Oct, 2023 by Irvene Kwambana
    Reading the training data set. 
    """
    dfx = pd.read_csv('static/Diabetes_XTrain.csv')
    dfy = pd.read_csv('static/Diabetes_YTrain.csv')
    X = dfx.values
    Y = dfy.values
    Y = Y.reshape((-1,))

    """ 
    20:18:20 09 Oct, 2023 by Irvene Kwambana
    Reading data from user. 
    """
    value = ''
    if request.method == 'POST':

        pregnancies = float(request.POST['pregnancies'])
        glucose = float(request.POST['glucose'])
        bloodpressure = float(request.POST['bloodpressure'])
        skinthickness = float(request.POST['skinthickness'])
        bmi = float(request.POST['bmi'])
        insulin = float(request.POST['insulin'])
        pedigree = float(request.POST['pedigree'])
        age = float(request.POST['age'])

        user_data = np.array(
            (pregnancies,
             glucose,
             bloodpressure,
             skinthickness,
             bmi,
             insulin,
             pedigree,
             age)
        ).reshape(1, 8)

        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X, Y)

        predictions = knn.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"

    return render(request,
                  'diabetes.html',
                  {
                      'result': value,
                      'title': 'Diabetes Disease Prediction',
                      'active': 'btn btn-success peach-gradient text-white',
                      'diabetes': True,
                      'form': DiabetesForm(),
                  }
                  )


def breast(request):
    """ 
    20:56:20 09 Oct, 2023 by Irvene Kwambana
    Reading training data set. 
    """
    df = pd.read_csv('static/Breast_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1]
    print(X.shape, Y.shape)

    """ 
    20:57:20 09 Oct, 2023 by Irvene Kwambana
    Reading data from user. 
    """
    value = ''
    if request.method == 'POST':

        radius = float(request.POST['radius'])
        texture = float(request.POST['texture'])
        perimeter = float(request.POST['perimeter'])
        area = float(request.POST['area'])
        smoothness = float(request.POST['smoothness'])

        """ 
        21:02:21 09 Oct, 2019 by Irvene Kwamabana
        Creating our training model. 
        """
        rf = RandomForestClassifier(
            n_estimators=16, criterion='entropy', max_depth=5)
        rf.fit(np.nan_to_num(X), Y)

        user_data = np.array(
            (radius,
             texture,
             perimeter,
             area,
             smoothness)
        ).reshape(1, 5)

        predictions = rf.predict(user_data)
        print(predictions)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don\'t have"

    return render(request,
                  'breast.html',
                  {
                      'result': value,
                      'title': 'Breast Cancer Prediction',
                      'active': 'btn btn-success peach-gradient text-white',
                      'breast': True,
                      'form': BreastCancerForm(),
                  })


""" 
20:07:20 10 Oct, 2023 by Irvene Kwambana
Handling 404 error pages. 
"""


def handler404(request):
    return render(request, '404.html', status=404)
