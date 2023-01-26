from rest_framework.views import APIView
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Questions,Profile,Answers
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
import json
# Create your views here. 

# def signin(request):
#     return render(request,"signin.html")

@login_required(login_url='/')
def home(request):
    return render(request,"home.html")


def logout_user(request):
    logout(request)
    return redirect("signin")

def signin(request):
    ctx = {}
    if request.session.get("signupsuccess"):
        ctx["signupsuccess"] = request.session.get("signupsuccess")
        del request.session["signupsuccess"]
    if request.method == "POST":
        username = request.POST["signinemail"]
        password = request.POST["signinpassword"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            request.session["signupsuccess"] = "Wrong credentials"
            return redirect('login')
    return render(request, "signin.html", ctx)

def signup(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email

        if User.objects.filter(email=email):
            request.session["signupsuccess"] = "Email already exist! Please try some other Email"
            return redirect('signin')
        x = User.objects.create_user(username=username, email=email, password=password)
        x.save()
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            y = Profile()
            y.user = request.user
            y.name = name
            y.phone = phone
            y.save()
            return redirect('home')
        request.session["signupsuccess"] = "Sign up Successfully, You can login now"
        return redirect('signin')
    return render(request, "signin.html")


@login_required(login_url='/')
def myQuestion(request):
    ctx = {}
    temp = {}
    r = Questions.objects.filter(user=request.user)
    for i in r:
        dic = {}
        rtt = Answers.objects.filter(question=i)
        for j in rtt:
            if j.answers in dic:
                dic[j.answers] +=1
            else:
                dic[j.answers] = 1
        sorted_dic = {k: v for k, v in sorted(dic.items(), reverse=True, key=lambda item: item[1])}
        if len(list(sorted_dic.values())) == 0:
            temp[i.id] = "No Response"
            continue
        highest = list(sorted_dic.values())[0]
        final_dic = {k:v for k,v in sorted_dic.items() if v == highest}
        answer = ','.join(final_dic.keys())
        temp[i.id] = answer
        
    ctx["myquestions"] = r
    ctx["answers_response"] = temp
    print(ctx)
    return render(request,'myquestions.html', ctx)


@login_required(login_url='/')
def allQuestion(request):
    ctx = {}
    ctx["allquestions"] = Questions.objects.all()
    return render(request,'allquestions.html',ctx)
    
    
@login_required(login_url='/')
def askQuestion(request):
    ctx = {}
    if request.session.get("message"):
        ctx["message"] = request.session.get("message")
        del request.session["message"]
    
    if request.method == 'POST':
        question = request.POST.get('question')
        first_option = request.POST.get('first_option')
        second_option = request.POST.get('second_option')
        third_option = request.POST.get('third_option')
        fourth_option = request.POST.get('fourth_option')
        if Questions.objects.filter(user=request.user).count() >= 5:
            request.session["message"] = "You have crossed the limit"
            return redirect("askQuestion")
        else:
            x = Questions()
            x.user = request.user
            x.question = question
            x.first_option = first_option
            x.second_option = second_option
            x.third_option = third_option
            x.fourth_option = fourth_option
            x.save()
            request.session["message"] = "Added Successfully"
            return redirect("askQuestion")
    return render(request,'askquestion.html', ctx)


@login_required(login_url='/')
def profile(request):
    x = Profile.objects.get(user=request.user)
    answered = Answers.objects.filter(user=request.user).count()
    asked = Questions.objects.filter(user=request.user).count()
    ctx = {}
    ctx["name"] = x.name
    ctx["phone"] = x.phone
    ctx["answered"] = answered
    ctx["asked"] = asked
    return render(request,"profile.html",ctx)



class MarkAnswer(APIView):
    def post(self,request):
        ctx = {}
        id = request.data.get("id")
        answer = request.data.get("answer")
        ques = Questions.objects.get(pk=id)
        if Answers.objects.filter(user=request.user,question=ques).exists():
            x = Answers.objects.get(user=request.user,question=ques)
            x.answers = answer
            x.save()
        else:
            x = Answers()
            x.user = request.user
            x.question = Questions.objects.get(pk=id)
            x.answers = answer
            x.save()
        ctx["success"] = "Marked Successfully" 
        return HttpResponse(json.dumps(ctx),content_type="application/json")
        return Response(ctx,status=status.HTTP_201_CREATED)
        
        

class GetAnswer(APIView):
    def get(self,request):
        ctx = {}
        temp = {}
        r = Questions.objects.filter(user=request.user)
        for i in r:
            dic = {}
            rtt = Answers.objects.filter(question=i)
            for j in rtt:
                if j.answers in dic:
                    dic[j.answers] +=1
                else:
                    dic[j.answers] = 1
            sorted_dic = {k: v for k, v in sorted(dic.items(), reverse=True, key=lambda item: item[1])}
            if len(list(sorted_dic.values())) == 0:
                temp[i.id] = "No Response"
                continue
            highest = list(sorted_dic.values())[0]
            final_dic = {k:v for k,v in sorted_dic.items() if v == highest}
            answer = ','.join(final_dic.keys())
            temp[str(i.id)] = answer
            
        ctx["answers_response"] = temp
        # return HttpResponse(json.dumps(ctx),content_type="application/json")
        return Response(ctx,status=status.HTTP_201_CREATED)
        
