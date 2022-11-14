from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from django.http import HttpResponse

from .models import *
from users.models import user_votes
from foodcourt.settings import BASE_DIR
# Create your views here.

def index(request):
    # request.session["login_status"] = False
    # login_status = request.session["login_status"]
    return render(request, 'index.html')

def leaderboard(request):
    dish = dishes.objects.all()
    print("All dishes")
    print(dish)
    return render(request, 'leaderboard.html', {'dish': dish, 'BASE_DIR':BASE_DIR})

enable = True

def v_valid(request, dish_Id):
    if date.today():
        # u_vote = user_votes.objects.all()
        user_email = request.session["user_email"]

        u_vote = user_votes.objects.get(user_Id=user_email)
        if u_vote:
            enable = True
        else:
            enable = False

@login_required(login_url='/login')
def dish_details(request, dish_Id):
    dish = dishes.objects.get(dish_Id=dish_Id)
    user_email = request.session["user_email"]
    print(user_email)

    vote = user_votes.objects.all()
    print(len(vote))
    # vote = user_votes.objects.get(user_Id=user_email)



    return render(request,'menu1.html', {'dish': dish, 'user_email':user_email, 'enable':enable, 'BASE_DIR':BASE_DIR})



def dishAdd(request):
    if request.method == 'POST':
        dish_Data = dishes()
        dish_Data.d_Name = request.POST.get("dName", False)
        dish_Data.d_Description = request.POST.get("dDescription", False)
        dish_Data.d_Ingredients = request.POST.get("dIngredients", False)
        dish_Data.d_Type = request.POST.get("dtype", False)
        dish_Data.d_Photo = request.FILES.get("dPhoto", False)

        print("dish_Data")
        print(dish_Data.d_Name)
        print(dish_Data.d_Description)
        print(dish_Data.d_Ingredients)
        print(dish_Data.d_Photo)

        dish_Data.save()
        messages.success(request, "Your Dish Added Successfully")
    return render(request, 'dish_add.html')