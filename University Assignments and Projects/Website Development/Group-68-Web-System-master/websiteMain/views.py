from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
# Create your views here.
from email.policy import strict
from .models import *
from itertools import chain


#Main View Patterns


def index(request):

	#return render(request, 'websiteMain/index.html')

	#return render(request, 'websiteMain/index.html')
	#return HttpResponse('<p>Hello World</p>')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/information')
			else:
				return HttpResponse("Your account is disabled")
		else:
			#print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")

	
	return render(request, 'websiteMain/index.html')

@login_required	
def information(request):
	malls = Mall.objects.all()
	hotels = Hotel.objects.all()
	parks = Park.objects.all()
	colleges = College.objects.all()
	libararies = Library.objects.all()
	zoos = Zoo.objects.all()
	museums = Museum.objects.all()
	industries = Industry.objects.all()
	restaurants = Restaurant.objects.all()
	
	template = loader.get_template('websiteMain/information.html')
	places = list(chain(malls, hotels, parks, colleges, libararies, zoos, museums, industries, restaurants))
	context = {
		'results': places
	}
	return HttpResponse(template.render(context, request))

def help(request):
	return render(request, 'websiteMain/help.html')

@login_required	
def categories(request):
	q1 = Mall.objects.all()
	q2 = Hotel.objects.all()
	q3 = Park.objects.all()
	q4 = College.objects.all()
	q5 = Library.objects.all()
	q6 = Zoo.objects.all()
	q7 = Museum.objects.all()
	q8 = Industry.objects.all()
	q9 = Restaurant.objects.all()
	
	template = loader.get_template('websiteMain/results.html')
	query = request.GET.get("query")
	
	if query:
		#queryset_list = queryset_list.filter(name__icontains=query)
		q1 = q1.filter(name__icontains=query)
		q2 = q2.filter(name__icontains=query)
		q3 = q3.filter(name__icontains=query)
		q4 = q4.filter(name__icontains=query)
		q5 = q5.filter(name__icontains=query)
		q6 = q6.filter(name__icontains=query)
		q7 = q7.filter(name__icontains=query)
		q8 = q8.filter(name__icontains=query)
		q9 = q9.filter(name__icontains=query)
		
		queryset_list=list(chain(q1, q2, q3, q4, q5, q6, q7, q8, q9))
		context = {
		'query': query,
		'results': queryset_list
		}
		return HttpResponse(template.render(context, request))
	else: 
		context = ['College','Library','Industry',
		'Hotel','Park','Zoo','Museum','Restaurant','Mall']
		return render(request, 'websiteMain/categories.html', {'categories': context})
	
def contacts(request):
	#[image of person, name, email]
	context = [['https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Nicolas_Cage_2011_CC.jpg/220px-Nicolas_Cage_2011_CC.jpg','Patrick ​Breen','n9726306@qut.edu.au', 'Client/Product Owner'],
			['https://tjbrearton.files.wordpress.com/2013/01/seenosideburns.jpg','Douglas ​Brennan','n7326645@qut.edu.au', 'Developer'],
			['http://howditgetburned.weebly.com/uploads/2/9/4/4/29441825/3592426_orig.jpg','Nicholas ​Constantine','nickconstantine3@gmail.com', 'Developer'],
			['http://images4.static-bluray.com/products/22/131_1_front.jpg','Joshua ​Stephens','n9707204@qut.edu.au', 'Scrum Master'],
			['http://i.dailymail.co.uk/i/pix/2007/04_03/NicolasCageAP_228x332.jpg','Tuan ​Luong','n5702747@qut.edu.au', 'Developer']]
	return render(request, 'websiteMain/contacts.html', {'names': context})
	
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save(commit=False)

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        #else:
         #   print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        

    # Render the template depending on the context.
    return render(request,
            'websiteMain/register.html',
            {'user_form': user_form, 'registered': registered} )

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/information')
			else:
				return HttpResponse("Your account is disabled")
		else:
			#print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'websiteMain/login.html')
		
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

#Create, Update, Delete items

class MallCreate(CreateView):
	model = Mall
	template_name = 'websiteMain/mall_form.html'
	fields = ['name','address','phone_number','city','email','image_url']

class MallUpdate(UpdateView):
	model = Mall
	template_name = 'websiteMain/mall_form.html'
	fields = ['name','address','phone_number','city','email','image_url']

class MallDelete(DeleteView):
	model = Mall
	success_url = reverse_lazy('websiteMain/index')

#Profile
def profile(request):
	return render(request, 'websiteMain/profile.html')

#Submit Profile Changes
#def SubmitProfileChanges(request):


#Data View Patterns

#Shows all the malls stored in the DB
@login_required
def malls(request):
	all_malls = Mall.objects.all()
	template = loader.get_template('websiteMain/information_malls.html')
	context = {
		'all_malls': all_malls
	}
	return HttpResponse(template.render(context, request))

#Shows a mall using its mall_ID
@login_required
def mall_detail(request, mall_id):
	mall = Mall.objects.get(id=mall_id)
	mall_rev = Review_Mall.objects.filter(mall = mall_id)
	template = loader.get_template('websiteMain/mallGet.html')
	context = {
		'mall': mall,
		'mall_rev': mall_rev,
	}
	return HttpResponse(template.render(context, request))

	
#Shows all the hotels stored in the DB
@login_required
def hotels(request):
	all_hotels = Hotel.objects.all()
	template = loader.get_template('websiteMain/information_hotels.html')
	context = {
		'all_hotels': all_hotels
	}
	return HttpResponse(template.render(context, request))

#Shows a hotel using its hotel_ID
@login_required
def hotel_detail(request, hotel_id):
	hotel = Hotel.objects.get(id=hotel_id)
	hotel_rev = Review_Hotel.objects.filter(hotel = hotel_id)
	template = loader.get_template('websiteMain/hotelGet.html')
	context = {
		'hotel': hotel,
		'hotel_rev': hotel_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the parks stored in the DB
@login_required
def parks(request):
	all_parks = Park.objects.all()
	template = loader.get_template('websiteMain/information_parks.html')
	context = {
		'all_parks': all_parks
	}
	return HttpResponse(template.render(context, request))

#Shows a park using its park_ID
@login_required
def park_detail(request, park_id):
	park = Park.objects.get(id=park_id)
	park_rev = Review_Park.objects.filter(park = park_id)
	template = loader.get_template('websiteMain/parkGet.html')
	context = {
		'park': park,
		'park_rev': park_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the colleges stored in the DB
@login_required
def colleges(request):
	all_colleges = College.objects.all()
	template = loader.get_template('websiteMain/information_colleges.html')
	context = {
		'all_colleges': all_colleges
	}
	return HttpResponse(template.render(context, request))

#Shows a college using its college_ID
@login_required
def college_detail(request, college_id):
	college = College.objects.get(id=college_id)
	college_rev = Review_College.objects.filter(college = college_id)
	template = loader.get_template('websiteMain/collegeGet.html')
	context = {
		'college': college,
		'college_rev': college_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the libraries stored in the DB
@login_required
def libraries(request):
	all_libraries = Library.objects.all()
	template = loader.get_template('websiteMain/information_libraries.html')
	context = {
		'all_libraries': all_libraries
	}
	return HttpResponse(template.render(context, request))

#Shows a library using its library_ID
@login_required
def library_detail(request, library_id):
	library = Library.objects.get(id=library_id)
	library_rev = Review_Library.objects.filter(library = library_id)
	template = loader.get_template('websiteMain/libraryGet.html')
	context = {
		'library': library,
		'library_rev': library_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the zoos stored in the DB
@login_required
def zoos(request):
	all_zoos = Zoo.objects.all()
	template = loader.get_template('websiteMain/information_zoos.html')
	context = {
		'all_zoos': all_zoos
	}
	return HttpResponse(template.render(context, request))

#Shows a zoo using its zoo_ID
@login_required
def zoo_detail(request, zoo_id):
	zoo = Zoo.objects.get(id=zoo_id)
	zoo_rev = Review_Zoo.objects.filter(zoo = zoo_id)
	template = loader.get_template('websiteMain/zooGet.html')
	context = {
		'zoo': zoo,
		'zoo_rev': zoo_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the museums stored in the DB
@login_required
def museums(request):
	all_museums = Museum.objects.all()
	template = loader.get_template('websiteMain/information_museums.html')
	context = {
		'all_museums': all_museums
	}
	return HttpResponse(template.render(context, request))

#Shows a museum using its museum_ID
@login_required
def museum_detail(request, museum_id):
	museum = Museum.objects.get(id=museum_id)
	museum_rev = Review_Museum.objects.filter(museum = museum_id)
	template = loader.get_template('websiteMain/museumGet.html')
	context = {
		'museum': museum,
		'museum_rev': museum_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the industries stored in the DB
@login_required
def industries(request):
	all_industries = Industry.objects.all()
	template = loader.get_template('websiteMain/information_industries.html')
	context = {
		'all_industries': all_industries
	}
	return HttpResponse(template.render(context, request))

#Shows a industry using its industry_ID
@login_required
def industry_detail(request, industry_id):
	industry = Industry.objects.get(id=industry_id)
	industry_rev = Review_Industry.objects.filter(industry = industry_id)
	template = loader.get_template('websiteMain/industryGet.html')
	context = {
		'industry': industry,
		'industry_rev': industry_rev,
	}
	return HttpResponse(template.render(context, request))

#Shows all the restaurants stored in the DB
@login_required
def restaurants(request):
	all_restaurants = Restaurant.objects.all()
	template = loader.get_template('websiteMain/information_restaurants.html')
	context = {
		'all_restaurants': all_restaurants
	}
	return HttpResponse(template.render(context, request))

#Shows a restaurant using its restaurant_ID
@login_required
def restaurant_detail(request, restaurant_id):
	restaurant = Restaurant.objects.get(id=restaurant_id)
	restaurant_rev = Review_Restaurant.objects.filter(restaurant = restaurant_id)
	template = loader.get_template('websiteMain/restaurantGet.html')
	context = {
		'restaurant': restaurant,
		'restaurant_rev': restaurant_rev,
	}
	return HttpResponse(template.render(context, request))
	
@login_required
def favourites(request):
	mall_fav = Mall_Favourites.objects.all()
	hotel_fav = Hotel_Favourites.objects.all()
	park_fav = Park_Favourites.objects.all()
	college_fav = College_Favourites.objects.all()
	library_fav = Library_Favourites.objects.all()
	zoo_fav = Zoo_Favourites.objects.all()
	museum_fav = Museum_Favourites.objects.all()
	industry_fav= Industry_Favourites.objects.all()
	restaurant_fav = Restaurant_Favourites.objects.all()
	malls = Mall.objects.all()
	hotels = Hotel.objects.all()
	parks = Park.objects.all()
	colleges = College.objects.all()
	libraries = Library.objects.all()
	zoos = Zoo.objects.all()
	museums = Museum.objects.all()
	industries = Industry.objects.all()
	restaurants = Restaurant.objects.all()
	
	template = loader.get_template('websiteMain/favourites.html')
	
	context = {
		'mall_fav': mall_fav,
		'hotel_fav': hotel_fav,
		'park_fav': park_fav,
		'college_fav': college_fav,
		'library_fav': library_fav,
		'zoo_fav': zoo_fav,
		'museum_fav': museum_fav,
		'industry_fav': industry_fav,
		'restaurant_fav': restaurant_fav,
		'malls': malls,
		'hotels': hotels,
		'parks': parks,
		'colleges': colleges,
		'libraries': libraries,
		'zoos': zoos,
		'museums': museums,
		'industries': industries,
		'restaurants': restaurants
	}
	return HttpResponse(template.render(context, request))
	
@login_required
def favourite_mall(request, mall_id, user_id):
	in_table = False
	mall_fav = Mall_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	mall_input = Mall.objects.get(pk = mall_id)
	
	for mall in mall_fav:
		if user_input.id == mall.user_id and mall_input.id == mall.mall_id:
			
			Mall_Favourites.objects.filter(id = mall.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Mall_Favourites.objects.create(mall = Mall.objects.get(pk = mall_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_hotel(request, hotel_id, user_id):
	in_table = False
	hotel_fav = Hotel_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	hotel_input = Hotel.objects.get(pk = hotel_id)
	
	for hotel in hotel_fav:
		if user_input.id == hotel.user_id and hotel_input.id == hotel.hotel_id:
			
			Hotel_Favourites.objects.filter(id = hotel.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Hotel_Favourites.objects.create(hotel = Hotel.objects.get(pk = hotel_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_park(request, park_id, user_id):
	in_table = False
	park_fav = Park_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	park_input = Park.objects.get(pk = park_id)
	
	for park in park_fav:
		if user_input.id == park.user_id and park_input.id == park.park_id:
			
			Park_Favourites.objects.filter(id = park.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Park_Favourites.objects.create(park = Park.objects.get(pk = park_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_college(request, college_id, user_id):
	in_table = False
	college_fav = College_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	college_input = College.objects.get(pk = college_id)
	
	for college in college_fav:
		if user_input.id == college.user_id and college_input.id == college.college_id:
			
			College_Favourites.objects.filter(id = college.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = College_Favourites.objects.create(college = College.objects.get(pk = college_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_library(request, library_id, user_id):
	in_table = False
	library_fav = Library_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	library_input = Library.objects.get(pk = library_id)
	
	for library in library_fav:
		if user_input.id == library.user_id and library_input.id == library.library_id:
			
			Library_Favourites.objects.filter(id = library.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Library_Favourites.objects.create(library = Library.objects.get(pk = library_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_zoo(request, zoo_id, user_id):
	in_table = False
	zoo_fav = Zoo_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	zoo_input = Zoo.objects.get(pk = zoo_id)
	
	for zoo in zoo_fav:
		if user_input.id == zoo.user_id and zoo_input.id == zoo.zoo_id:
			
			Zoo_Favourites.objects.filter(id = zoo.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Zoo_Favourites.objects.create(zoo = Zoo.objects.get(pk = zoo_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_museum(request, museum_id, user_id):
	in_table = False
	museum_fav = Museum_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	museum_input = Museum.objects.get(pk = museum_id)
	
	for museum in museum_fav:
		if user_input.id == museum.user_id and museum_input.id == museum.museum_id:
			
			Museum_Favourites.objects.filter(id = museum.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Museum_Favourites.objects.create(museum = Museum.objects.get(pk = museum_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_industry(request, industry_id, user_id):
	in_table = False
	industry_fav = Industry_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	industry_input = Industry.objects.get(pk = industry_id)
	
	for industry in industry_fav:
		if user_input.id == industry.user_id and industry_input.id == industry.industry_id:
			
			Industry_Favourites.objects.filter(id = industry.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Industry_Favourites.objects.create(industry = Industry.objects.get(pk = industry_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def favourite_restaurant(request, restaurant_id, user_id):
	in_table = False
	restaurant_fav = Restaurant_Favourites.objects.all()
	user_input = User.objects.get(pk = user_id)
	restaurant_input = Restaurant.objects.get(pk = restaurant_id)
	
	for restaurant in restaurant_fav:
		if user_input.id == restaurant.user_id and restaurant_input.id == restaurant.restaurant_id:
			
			Restaurant_Favourites.objects.filter(id = restaurant.id).delete()
			#malls.save()
			in_table = True
			break
	
	if in_table == False:
		instance = Restaurant_Favourites.objects.create(restaurant = Restaurant.objects.get(pk = restaurant_id), user = User.objects.get(pk = user_id))
		instance.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required	
def review_college(request, college_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	college_rev = Review_College.objects.all()
	user_input = User.objects.get(pk = user_id)
	college_input = College.objects.get(pk = college_id)
	
	for college in college_rev:
		if user_input.id == college.user_id and college_input.id == college.college_id:
			
			Review_College.objects.filter(id = college.id).delete()
			break
	
	
	instance = Review_College.objects.create(user = User.objects.get(pk = user_id), college = College.objects.get(pk = college_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'college_ID',
		'id': college_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_library(request, library_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	library_rev = Review_Library.objects.all()
	user_input = User.objects.get(pk = user_id)
	library_input = Library.objects.get(pk = library_id)
	
	for library in library_rev:
		if user_input.id == library.user_id and library_input.id == library.library_id:
			
			Review_Library.objects.filter(id = library.id).delete()
			break
	
	
	instance = Review_Library.objects.create(user = User.objects.get(pk = user_id), library = Library.objects.get(pk = library_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'library_ID',
		'id': library_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_industry(request, industry_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	industry_rev = Review_Industry.objects.all()
	user_input = User.objects.get(pk = user_id)
	industry_input = Industry.objects.get(pk = industry_id)
	
	for industry in industry_rev:
		if user_input.id == industry.user_id and industry_input.id == industry.industry_id:
			
			Review_Industry.objects.filter(id = industry.id).delete()
			break
	
	
	instance = Review_Industry.objects.create(user = User.objects.get(pk = user_id), industry = Industry.objects.get(pk = industry_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'industry_ID',
		'id': industry_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_hotel(request, hotel_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	hotel_rev = Review_Hotel.objects.all()
	user_input = User.objects.get(pk = user_id)
	hotel_input = Hotel.objects.get(pk = hotel_id)
	
	for hotel in hotel_rev:
		if user_input.id == hotel.user_id and hotel_input.id == hotel.hotel_id:
			
			Review_Hotel.objects.filter(id = hotel.id).delete()
			break
	
	
	instance = Review_Hotel.objects.create(user = User.objects.get(pk = user_id), hotel = Hotel.objects.get(pk = hotel_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'hotel_ID',
		'id': hotel_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_park(request, park_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	park_rev = Review_Park.objects.all()
	user_input = User.objects.get(pk = user_id)
	park_input = Park.objects.get(pk = park_id)
	
	for park in park_rev:
		if user_input.id == park.user_id and park_input.id == park.park_id:
			
			Review_Park.objects.filter(id = park.id).delete()
			break
	
	
	instance = Review_Park.objects.create(user = User.objects.get(pk = user_id), park = Park.objects.get(pk = park_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'park_ID',
		'id': park_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_zoo(request, zoo_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	zoo_rev = Review_Zoo.objects.all()
	user_input = User.objects.get(pk = user_id)
	zoo_input = Zoo.objects.get(pk = zoo_id)
	
	for zoo in zoo_rev:
		if user_input.id == zoo.user_id and zoo_input.id == zoo.zoo_id:
			
			Review_Zoo.objects.filter(id = zoo.id).delete()
			break
	
	
	instance = Review_Zoo.objects.create(user = User.objects.get(pk = user_id), zoo = Zoo.objects.get(pk = zoo_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'zoo_ID',
		'id': zoo_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_museum(request, museum_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	museum_rev = Review_Museum.objects.all()
	user_input = User.objects.get(pk = user_id)
	museum_input = Museum.objects.get(pk = museum_id)
	
	for museum in museum_rev:
		if user_input.id == museum.user_id and museum_input.id == museum.museum_id:
			
			Review_Museum.objects.filter(id = museum.id).delete()
			break
	
	
	instance = Review_Museum.objects.create(user = User.objects.get(pk = user_id), museum = Museum.objects.get(pk = museum_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'museum_ID',
		'id': museum_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_restaurant(request, restaurant_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	restaurant_rev = Review_Restaurant.objects.all()
	user_input = User.objects.get(pk = user_id)
	restaurant_input = Restaurant.objects.get(pk = restaurant_id)
	
	for restaurant in restaurant_rev:
		if user_input.id == restaurant.user_id and restaurant_input.id == restaurant.restaurant_id:
			
			Review_Restaurant.objects.filter(id = restaurant.id).delete()
			break
	
	
	instance = Review_Restaurant.objects.create(user = User.objects.get(pk = user_id), restaurant = Restaurant.objects.get(pk = restaurant_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'restaurant_ID',
		'id': restaurant_id,
		}
	return HttpResponse(template.render(context, request))

@login_required	
def review_mall(request, mall_id, user_id):
	score_id = request.GET.get('score')
	comment_id = request.GET.get('comment')
	mall_rev = Review_Mall.objects.all()
	user_input = User.objects.get(pk = user_id)
	mall_input = Mall.objects.get(pk = mall_id)
	
	for mall in mall_rev:
		if user_input.id == mall.user_id and mall_input.id == mall.mall_id:
			
			Review_Mall.objects.filter(id = mall.id).delete()
			break
	
	
	instance = Review_Mall.objects.create(user = User.objects.get(pk = user_id), mall = Mall.objects.get(pk = mall_id), user_name = user_input.username, comment = comment_id, rating = score_id)
	instance.save()

	template = loader.get_template('websiteMain/review_submitted.html')
	context = {
		'ID': 'mall_ID',
		'id': mall_id,
		}
	return HttpResponse(template.render(context, request))