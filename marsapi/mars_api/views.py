from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime

import requests
import json

# Create your views here.


def home(request):
    landing_date = datetime(2012, 8, 6) 
    current_date = datetime.now()
    delta = current_date - landing_date
    current_sol = delta.days
    
    response = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=3974&api_key=' + settings.NASA_API_KEY)
    
    
    print(f"NASA_API_KEY: {settings.NASA_API_KEY}")
    print(f"Response: {response}")
    
    loaded_json = json.loads(response.text)
    print(f"loaded_json: {loaded_json}")
    max_sol = loaded_json['photos'][0]['rover']['max_sol']
    images_list = []
    for i in range(max_sol, max_sol - 7, -1):
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={i}&api_key={settings.NASA_API_KEY}')        
        if response.status_code == 200:
            loaded_json = json.loads(response.text)
            if 'photos' in loaded_json and len(loaded_json['photos']) > 0:
                img_src = loaded_json['photos'][0]['img_src']
                earth_date = loaded_json['photos'][0]['earth_date']
                date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
                earth_date = date_obj.strftime("%d/%m/%Y")
                sol = loaded_json['photos'][0]['sol']
                images_list.append({'img_src': img_src, 'earth_date': earth_date, 'sol': sol})
            
    print(f"images_list: {images_list}")

    #try:
    #    img_src = loaded_json['photos'][0]['img_src']
    #    earth_date = loaded_json['photos'][0]['earth_date']
    #    date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
    #    earth_date = date_obj.strftime("%d/%m/%Y")
    #    sol = loaded_json['photos'][0]['sol']#

        #daily_image = loaded_json.get('url')
        #print(f"daily_image: {daily_image}")
    #except IndexError:
        # Gestisci l'errore qui
    #    img_src = ""
    #    earth_date = "Il giorno richiesto non esiste"
    #    sol = "Il sol richiesto non esiste"
    
    

    #title = loaded_json.get('title')
    #explanation = loaded_json.get('explanation')
    #date = loaded_json.get('date')
    #owner = loaded_json.get('copyright')

    context = {
        #'img_src': img_src,
        #'earth_date': earth_date,
        #'sol': sol,
        'images_list': images_list,
        #'title':title,
        #'explanation':explanation,
        #'date':date,
        #'owner':owner
    }

    return render(request, "mars_api/home.html", context)
