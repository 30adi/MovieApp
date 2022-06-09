from django.shortcuts import render
import requests
import pyrebase
from omdb import OMDBClient
import random


Config = {
  'apiKey': "AIzaSyC-jhr5utEUYnqK1sfgnc8pSRaBifDRHog",
    'authDomain': "movie-f4e8b.firebaseapp.com",
    'projectId': "movie-f4e8b",
    'storageBucket': "movie-f4e8b.appspot.com",
    'messagingSenderId': "359849985960",
    'appId': "1:359849985960:web:7ccdc7c56a9c0b8d3bbf9d",
    'measurementId': "G-C53JWXDZ42",
    'databaseURL' : "https://movie-f4e8b-default-rtdb.firebaseio.com",
}
firebase = pyrebase.initialize_app(Config)
database = firebase.database()
authe = firebase.auth()

client = OMDBClient(apikey=38682202)


# Create your views here.


def apidata(request):
    try:
        movieName = request.POST['search']
        apiKey = '3950fb0d'
        base_url = 'https://www.omdbapi.com/?'
        apidata.url = base_url + "t="+movieName + "&apikey="+apiKey
        response = requests.get(apidata.url)
        movie_json = response.json()
        movieName = movieName.replace(movieName, movie_json['Title'])
        database.child('Movie').child('Movie Name').push({'name': movieName})
        return render(request,"postsearch.html", movie_json)
    except:
        message = "Movie not found !"
        return render(request, "index.html", {"msg": message})

def home(request):
    # render function takes argument  - request
    # and return HTML as response
    mnames_list = []
    mnames = database.child('Movie').child('Movie Name').get()
    for i in mnames:
        mnames_list.append(i.val()['name'])
    mnames_list=set(mnames_list)
    rndm_movies=random.sample(list(mnames_list),12)
    homepage_list=[]
    for home_movie in rndm_movies:
        apiKey = '3950fb0d'
        base_url = 'https://www.omdbapi.com/?'
        apidata.url = base_url + "t=" + home_movie + "&apikey=" + apiKey
        response = requests.get(apidata.url)
        movie_json = response.json()
        homepage_list.append([home_movie,movie_json["Poster"],movie_json["imdbRating"]])
    return render(request, "index.html",{'n':homepage_list})


def movie_result(request):
    response = requests.get(apidata.url)
    movie_json = response.json()
    return render(request, 'movieresult.html',movie_json)

def index_to_movieresult(request,name):
    home_movie = name
    try:
        apiKey = '3950fb0d'
        base_url = 'https://www.omdbapi.com/?'
        apidata.url = base_url + "t=" + home_movie + "&apikey=" + apiKey
        response = requests.get(apidata.url)
        movie_json = response.json()
        index_movieName = home_movie.replace(home_movie, movie_json['Title'])
        database.child('Movie').child('Movie Name').push({'name': index_movieName})
        print(home_movie)
        return render(request, "postsearch.html", movie_json)

    except:
        message = "Movie not found !"
        print(message)
        return render(request, "index.html", {"msg": message})
