from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime
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
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)
    tomorrow = today + datetime.timedelta(days = 1) 
    dish = dishes.objects.all()
    print("All dishes")
    print(dish)
    return render(request, 'dishes.html', {'dish': dish, 'tomorrow':tomorrow, 'BASE_DIR':BASE_DIR})


def today_votes_dish():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)
    tomorrow = today + datetime.timedelta(days = 1) 
    print('Yesterday : ',yesterday)
    print('Today : ',today)
    print('Tomorrow : ',tomorrow)
    dish_Ids = []
    today_dish_votes = {}
    for i in user_votes.objects.all():
        if i.v_Date == date.today():
            if int(i.dish_Id) not in dish_Ids:
                dish_Ids.append(int(i.dish_Id))
    
    for di in dish_Ids:
        dv = 0
        for uv in user_votes.objects.all():
            if uv.v_Date == date.today() and int(uv.dish_Id) == di:
                dv+=1
        today_dish_votes[di] = dv
    print('Today Votes',today_dish_votes)
    


    return ''



# def v_valid(request, dish_Id):
#     if date.today():
#         # u_vote = user_votes.objects.all()
#         user_email = request.session["user_email"]

#         u_vote = user_votes.objects.get(user_Id=user_email)
#         if u_vote:
#             enable = True
#         else:
#             enable = False

@login_required(login_url='/login')
def dish_details(request, dish_Id):
    today_votes_dish()
    dish = dishes.objects.get(dish_Id=dish_Id)
    # user_email = request.session["user_email"]
    user_email = request.user.email
    print('Current User', user_email)
    print(user_email)
    # v_valid(request, dish_Id)
    enable = True
    u_vote = user_votes()
    d_vote = dish_votes()
    vd_list = []
    for v in dish_votes.objects.all():
        vd_list.append(int(v.dish_Id))
    vu_list = []
    for u in user_votes.objects.all():
        vd_list.append(u.user_Id)
        # print(u.user_Id)
    p_u_vote = user_votes.objects.all()
    print("Length of p votes", len(p_u_vote))
    print("Dhis ID", dish_Id, type(dish_Id))
    for i in p_u_vote:
        # print(type(i.dish_Id))
        if int(i.dish_Id) == dish_Id and i.v_Date == date.today():
            # print(i.v_Date)
            # enable = False
            # print(user_email)
            # print(i.user_Id)
            if i.user_Id == user_email:
                enable = False
                print(i.user_Id)



    vote = user_votes.objects.all()
    print(len(vote))
    # vote = user_votes.objects.get(user_Id=user_email)


    if request.method == 'POST':
        u_vote.user_Id = request.user.email
        u_vote.dish_Id = dish.dish_Id
        u_vote.dish_Name = dish.d_Name
        u_vote.save()

        if dish_Id in vd_list:
            all_vote = dish_votes.objects.get(dish_Id=dish_Id)
            d_vote.dish_Id = dish.dish_Id
            d_vote.d_Name = dish.d_Name
            d_vote.d_Votes = all_vote.d_Votes + 1
            d_vote.v_Date = date.today()
            d_vote.save()
        else:  #First Vote of a dish
            d_vote.dish_Id = dish.dish_Id
            d_vote.d_Name = dish.d_Name
            d_vote.d_Votes = 1
            d_vote.v_Date = date.today()
            d_vote.save()
        print("We Counted Your Vote")
        messages.success(request, "We Counted your Vote!")
        # enable = False
        return redirect('dishes:dish_details',dish_Id)



    return render(request,'menu1.html', {'dish': dish, 'user_email':user_email, 'enable':enable, 'BASE_DIR':BASE_DIR})


# def vote(request, dish_Id):
#     dish = dishes.objects.get(dish_Id=dish_Id)
#     u_vote = user_votes()
#     d_vote = dish_votes()
#     if enable:
#         u_vote.user_Id = request.session["user_email"]
#         u_vote.dish_Id = dish.dish_Id
#         u_vote.dish_Name = dish.d_Name
#         u_vote.save()

#         d_vote.dish_Id = dish.dish_Id
#         d_vote.d_Name = dish.d_Name
#         d_vote.save()
#         messages.success(request, "Your Dish Added Successfully")

#     return 



def dishAdd(request):
    if request.method == 'POST':
        dish_Data = dishes()
        dish_Data.d_Name = request.POST.get("dName", False)
        dish_Data.d_Description = request.POST.get("dDescription", False)
        dish_Data.d_Ingredients = request.POST.get("dIngredients", False)
        dish_Data.d_Price = request.POST.get("dPrice", False)
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