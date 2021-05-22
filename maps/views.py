from collections import Counter
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import json
import re
from itertools import islice
import base64

from .models import User, Map, Category, State, Country

class NewMapForm(forms.ModelForm):

    country_name = forms.ModelChoiceField(queryset=Country.objects.all().order_by("COUNTRY_NAME"), required=True,  widget= forms.Select(attrs={'class':'select-box grid_country_selection','id':'country_choice'}))
    state_name = forms.ModelChoiceField(queryset=State.objects.all(), required=True, widget= forms.Select(attrs={'class':'select-box grid_state_selection','id':'state_choice'}))

    class Meta:
        model = Map
        fields = ['map_data', 'title', 'description', 'country_name', 'state_name', 'starting_location', 'duration_hours', 'duration_minutes', 'distance', 'category', 'cover', 'long', 'small_1', 'small_2']
        widgets = {
            'map_data': forms.HiddenInput(attrs={'class':'map_data'}),
            'title': forms.TextInput(attrs={'class':'form-input-box grid_title', 'placeholder':'Name your walk!'}),
            'description': forms.Textarea(attrs={'class':'form-description grid_description', 'placeholder':'What makes this walk special?', 'style':'white-space: pre-wrap'}),
            'starting_location': forms.TextInput(attrs={'class':'form-input-box grid_starting-location', 'placeholder':'Which address should people start from?'}),
            'duration_hours': forms.NumberInput(attrs={'class':'form-input-box grid_duration', 'placeholder':'How many hours?', 'min': 0, 'max': 99}),
            'duration_minutes': forms.NumberInput(attrs={'class':'form-input-box grid_duration', 'placeholder':'How many minutes?', 'min': 0, 'max': 59}),
            'distance': forms.HiddenInput(attrs={'class':'map_data'}),
            'category': forms.Select(attrs={'class':'select-box grid_category'}),
            'cover': forms.FileInput(attrs={'class':'custom-file-input grid_cover'}),
            'long': forms.FileInput(attrs={'class':'custom-file-input grid_long'}),
            'small_1': forms.FileInput(attrs={'class':'custom-file-input grid_small1'}),
            'small_2': forms.FileInput(attrs={'class':'custom-file-input grid_small2'}), 
            }

class NewEditForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = ['title', 'description', 'starting_location', 'duration_hours', 'duration_minutes', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-input-box grid_title', 'placeholder':'Name your walk!'}),
            'description': forms.Textarea(attrs={'class':'form-description grid_description', 'placeholder':'What makes this walk special?', 'style':'white-space: pre-wrap'}),
            'starting_location': forms.TextInput(attrs={'class':'form-input-box grid_starting-location', 'placeholder':'Which address should people start from?'}),
            'duration_hours': forms.NumberInput(attrs={'class':'form-input-box grid_duration', 'placeholder':'How many hours?', 'min': 0, 'max': 99}),
            'duration_minutes': forms.NumberInput(attrs={'class':'form-input-box grid_duration', 'placeholder':'How many minutes?', 'min': 0, 'max': 59}),
            'category': forms.Select(attrs={'class':'select-box grid_category'}),
            }

class NewSearchForm(forms.Form):
    country_name = forms.ModelChoiceField(queryset=Country.objects.all().order_by("COUNTRY_NAME"), required=True,  widget= forms.Select(attrs={'class':'select-box grid_country_selection required','id':'country_choice'}))
    state_name = forms.ModelChoiceField(queryset=State.objects.all(), required=True, widget= forms.Select(attrs={'class':'select-box grid_state_selection required','id':'state_choice'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="None", required=False, widget=forms.Select(attrs={'class':'select-box grid_country_selection','id':'category_choice'}))


#works
@login_required(login_url='login')
def test(request):

    categories = Category.objects.all()

    country_list = Country.objects.all()

    context = {
        "categories": categories,
        "countries": country_list,
        "form": NewMapForm()
    }
    return render(request, 'maps/test.html', context)

def login_view(request):
    return render(request, 'maps/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def not_found(request):
    return render(request, 'maps/error_no_page_exists.html')

#works
#TODO - more features
def profile_page(request, profile):

    # Check if user exists
    try:
        user_exists = User.objects.get(username = profile)
    except:
        return HttpResponseRedirect(reverse('not_found'))

    # Get objects
    posts = Map.objects.filter(creator = user_exists).order_by('-time_created')

    for post in posts:
        distance_from_model = post.distance

        if (distance_from_model > 1):
            distance = round(distance_from_model, 1)
            distance = distance.normalize()
            post.distance = str(distance) + " kms"
        else:
            distance = distance_from_model * 1000
            distance = round(distance, 0)
            post.distance = str(distance) + " metres"

    # Pagify objects
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # Provide context
    context = {
        "maps": page,
        "creator_name": user_exists.username
    }

    return render(request, "maps/profile_page.html", context)

def search_results(request):

    print("-----------------------------------------------------------------")
    print("found the following information from URL parameters")
    print(request.GET)
    print("-----------------------------------------------------------------")

    query = request.GET.get("q", "")

    if query == "":
        # Isolate the data from the 'cleaned' version of form data
        country = request.GET.get("country_name", "")
        state = request.GET.get("state_name", "")
        category = request.GET.get("category", "")
    else:
        country = query[0]
        state = query[1]
        category = query[2]
        print("-----------------------------------------------------------------")
        print("on next page found the following in query object")
        print(country)
        print(state)
        print(category)
        print("-----------------------------------------------------------------")

    print("-----------------------------------------------------------------")
    print("confirm information received to query")
    print("-----------------------------------------------------------------")
    if country == "" or state =="":
        return render(request, "maps/no_results.html")

    print("-----------------------------------------------------------------")
    print("check for country object")
    print("-----------------------------------------------------------------")
    try:
        country_name_object = Country.objects.get(pk = country)
    except:
        return render(request, "maps/no_results.html")
    print("-----------------------------------------------------------------")
    print(country_name_object)
    print("-----------------------------------------------------------------")

    print("-----------------------------------------------------------------")
    print("check for state object")
    print("-----------------------------------------------------------------")
    try:
        # find state name foreign key entry          
        state_name_object = State.objects.get(pk=state)
    except:
         return render(request, "maps/no_results.html")
    print("-----------------------------------------------------------------")
    print(state_name_object)
    print("-----------------------------------------------------------------")

    if (category):
        maps = Map.objects.filter(country_name = country_name_object, state_name = state_name_object, category = category).order_by('-time_created')
    else:
        maps = Map.objects.filter(country_name = country_name_object, state_name = state_name_object).order_by('-time_created')

    print("-----------------------------------------------------------------")
    print("Found results of...")
    print(maps)
    print("Length of...")
    print(len(maps))
    print("-----------------------------------------------------------------")

    if (len(maps) > 0):
        for map in maps:
            distance_from_model = map.distance

            if (distance_from_model > 1):
                distance = round(distance_from_model, 1)
                distance = distance.normalize()
                map.distance = str(distance) + " kms"
            else:
                distance = distance_from_model * 1000
                distance = round(distance, 0)
                map.distance = str(distance) + " metres"

        print("-----------------------------------------------------------------")
        print("Paginated search results...")
        print("-----------------------------------------------------------------")

        # Pagify objects
        p = Paginator(maps, 10)
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        # Provide context
        context = {
            "maps": page,
            "search": True,
        }

        print("Load main search with context.")

        return render(request, "maps/search_results.html", context)
    else:
        return render(request, "maps/no_results.html")

#works
def search(request):

    if request.method == "GET":

        context = {
            "form": NewSearchForm(),
        }
        return render(request, 'maps/main_search.html', context)

#works
def home_page(request):

    maps = Map.objects.all().order_by('-time_created')

    for map in maps:
        distance_from_model = map.distance

        if (distance_from_model > 1):
            distance = round(distance_from_model, 1)
            distance = distance.normalize()
            map.distance = str(distance) + " kms"
        else:
            distance = distance_from_model * 1000
            distance = round(distance, 0)
            map.distance = str(distance) + " metres"


    # Pagify objects
    p = Paginator(maps, 10)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # Provide context
    context = {
        "maps": page,
    }

    return render(request, "maps/home_page.html", context)

#works
def display_map(request, map_id):

    try:
        map_object = Map.objects.get(pk=map_id)
    except:
        return render(request, 'maps/error_no_page_exists.html')

    distance_from_model = map_object.distance

    if (distance_from_model > 1):
        distance = round(distance_from_model, 1)
        distance = distance.normalize()
        distance = str(distance) + " kms"
    else:
        distance = distance_from_model * 1000
        distance = round(distance, 0)
        distance = str(distance) + " metres"

    context = {
        "map_id": map_id,
        "details": map_object,
        "distance": distance,
    }
    return render(request, 'maps/map.html', context)

#works
def geojson_search(request, map_id):

    if request.method == "GET":

        JSONstring = Map.objects.get(pk=map_id)

        #print("Found the following:")
        #print(JSONstring.map_data)

        JSONObject = json.loads(JSONstring.map_data)

        #print("JSONObject:")
        #print(JSONObject)

        return JsonResponse(JSONObject)

#works
def geojson(request):

    if request.method == "POST":

        print("-----------------------------------------------------------------")
        print("Received POST request")
        print("-----------------------------------------------------------------")

        # Take in the data the user submitted and save it as form
        form = NewMapForm(request.POST, request.FILES)

        print("-----------------------------------------------------------------")
        print("Check if form is valid")
        print("-----------------------------------------------------------------")

        # Check if form data is valid (server-side)
        if form.is_valid():

            print("-----------------------------------------------------------------")
            print("Form is valid")
            print("-----------------------------------------------------------------")

            # Isolate the data from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_location = form.cleaned_data["starting_location"]
            country_name = form.cleaned_data["country_name"]
            state_name = form.cleaned_data["state_name"]
            duration_hours = form.cleaned_data["duration_hours"]
            duration_minutes = form.cleaned_data["duration_minutes"]
            distance = form.cleaned_data["distance"]
            cover_image = form.cleaned_data["cover"]
            long_image = form.cleaned_data["long"]
            small_1_image = form.cleaned_data["small_1"]
            small_2_image = form.cleaned_data["small_2"]
            
            # find category foreign key entry
            category_object = Category.objects.get(id=form.cleaned_data["category"].id)

            # find category foreign key entry
            print("-----------------------------------------------------------------")
            print("found country name object")
            print(country_name)
            print("state name found from form prior to search")
            print(state_name)
            print("-----------------------------------------------------------------")            
            state_name_object = State.objects.get(STATE_NAME=state_name, CC_ISO=country_name.CC_ISO)

            print("-----------------------------------------------------------------")
            print("found state name object")
            print(state_name_object)
            print("-----------------------------------------------------------------")

            # process geoJSON into readable format
            unformatted_JSONstring = form.cleaned_data["map_data"]
            JSONstring = geoJSONconverter(unformatted_JSONstring)
            default_coordinates = default_coordinates_scanner(unformatted_JSONstring)
            
        else:
            print("-----------------------------------------------------------------")
            print("Form is not valid")
            print(form.errors)
            print("-----------------------------------------------------------------")

        print("-----------------------------------------------------------------")
        print("Found the following default coordinates")
        print(default_coordinates)
        print("-----------------------------------------------------------------")

        # if no coordinates found in the file return error
        if (default_coordinates == False):
            categories = Category.objects.all()

            context = {
                "categories": categories,
                "form": form
            }
            return render(request, 'maps/test.html', context)

        # create the new map
        new_map = Map(
            map_data=str(JSONstring), 
            creator=request.user,
            title=title,
            description=description,
            starting_location=starting_location,
            country_name=country_name,
            state_name=state_name_object,
            duration_hours=duration_hours,
            duration_minutes=duration_minutes,
            starting_location_1=default_coordinates[0],
            starting_location_2=default_coordinates[1],
            distance=distance,
            category=category_object,
            cover=cover_image,
            long=long_image,
            small_1=small_1_image,
            small_2=small_2_image) 
        new_map.save()

        map_id = str(new_map.id)
        print("-----------------------------------------------------------------")
        print("Successfully created new map!")
        print(new_map)
        print("Id:")
        print(map_id)
        print("-----------------------------------------------------------------")

        return HttpResponseRedirect(reverse('display_map', kwargs={'map_id':map_id}))

#Let's finish this one off
def edit_map(request, map_id):

    if request.method == "GET":
        try:
            map = Map.objects.get(pk=map_id)
        except:
            print("Was unable to delete that map as the server could not find it.")
            return render(request, "maps/error_no_page_exists.html")
        
        if request.user == map.creator:

            form = NewEditForm(instance=map) 

            context = {
                'map': map,
                'form': form,
            }

            return render(request, "maps/edit_map.html", context)
            
        else:
            print("Error - this is not the registered user for the map.")
            return render(request, "maps/error_no_page_exists.html")
    


#FINISHED
def geoJSONconverter(unformatted_string):

    # Replace the first "Type" with "type"

    modified_string = unformatted_string.replace('"Type"', '"type"', 1)

    # Testing
    i = 0
    contains = True

    # Replace 'null' with {}

    while (contains):
        if "null" in modified_string:
            i = i + 1
            print(i)
            modified_string = modified_string.replace('"properties":null', f'"properties":{{"name": "{i}"}}', 1)
        else:
            contains = False

    # Add quotes to the beginning and end to make it a string

    #modified_string = '\'' + modified_string + '\''

    return(modified_string)

#outdated now...
def REALgeoJSONconverter(unformatted_string):

    # Replace the first "Type" with "type"

    modified_string = unformatted_string.replace('"Type"', '"type"', 1)

    # Replace 'null' with {}

    modified_string = modified_string.replace('"properties":null', '"properties":{}')

    # Add quotes to the beginning and end to make it a string

    #modified_string = '\'' + modified_string + '\''

    return(modified_string)

#FINISHED
def default_coordinates_scanner(unformatted_string):
    print("-----------------------------------------------------------------")
    print("Scanning for default coordinates")
    print("-----------------------------------------------------------------")
    #default_coordinates = [] 
    starting_position = ["x", "y"]
    try:
        limit = 2
        counter = 0
        for i in islice(re.finditer(r"[+-]?\d+\.\d+", unformatted_string), limit):
            print(i.group())
            #default_coordinates.append(i.group())
            if counter == 0:
                starting_position[0] = i.group()
                counter = counter + 1
            if counter == 1:
                starting_position[1] = i.group()
    except:    
        starting_position = False

    if starting_position != False:
        #default_coordinates = str(default_coordinates).replace("'", "")
        starting_position[0] = float(starting_position[0])
        starting_position[1] = float(starting_position[1])

    return(starting_position)
        
#API to fetch state names
def state_names(request, country_name):


    print("==================================================")
    print("API has been called")
    print("==================================================")

    if request.method == "GET":

        print("==================================================")
        print("Verified that request.method is GET")
        print("==================================================")

        country = Country.objects.get(COUNTRY_NAME=country_name)
        country_code = country.CC_FIPS

        states = State.objects.filter(CC_FIPS=country_code).order_by("STATE_NAME")
        state_names = []
        state_pk = []

        for objects in states:
            state_names.append(objects.STATE_NAME)
            state_pk.append(objects.pk)

        state_object = [state_names, state_pk]

        print("==================================================")
        print("Generated state names of...")
        print(state_names)
        print("==================================================")

        return JsonResponse(state_object, safe=False)

#API to delete map
def delete_map(request, map_id):
    try:
        map = Map.objects.get(pk=map_id)
        user = map.creator.username
    except:
        print("Was unable to delete that map as the server could not find it.")
        return render(request, "maps/error_no_page_exists.html")

    if request.user == map.creator:
        print("Deleting map: " + str(map.pk))
        map.delete()
        print("Successfully deleted.")
        return HttpResponseRedirect(reverse("profile", kwargs={'profile':user}))
    else:
        return render(request, "maps/error_no_page_exists.html")

#API to save map changes made in edit screen
def save_map(request, map_id):
    try:
        map = Map.objects.get(pk=map_id)
        user = map.creator.username
    except:
        print("Was unable to delete that map as the server could not find it.")
        return render(request, "maps/error_no_page_exists.html")

    if request.user == map.creator:
        print("Editing map: " + str(map.pk))
        
        if request.method == "POST":

            form = NewEditForm(request.POST, request.FILES)

            if form.is_valid():

                print("-----------------------------------------------------------------")
                print("Form is valid")
                print("-----------------------------------------------------------------")

                # Isolate the data from the 'cleaned' version of form data
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                starting_location = form.cleaned_data["starting_location"]
                duration_hours = form.cleaned_data["duration_hours"]
                duration_minutes = form.cleaned_data["duration_minutes"]
                category_object = Category.objects.get(id=form.cleaned_data["category"].id)

                map.title = title
                map.description = description
                map.starting_location = starting_location
                map.duration_hours = duration_hours
                map.duration_minutes = duration_minutes
                map.category = category_object

                map.save()

                print("Successfully edited.")
                return HttpResponseRedirect(reverse("display_map", kwargs={'map_id':map.pk}))

            else:
                print("The form was not valid..")
                return render(request, "maps/error_no_page_exists.html")

        else:
            print("This request method was not post.")
            return render(request, "maps/error_no_page_exists.html")

    else:
        print("This user is not the registered creator of the map.")
        return render(request, "maps/error_no_page_exists.html")
