from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from django.core.cache import cache

import requests
import json

# Create your views here.


def home(request, rover_name='curiosity'):

    
    background_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={settings.NASA_API_KEY}')
    response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol=100&page=1&api_key={settings.NASA_API_KEY}')
    
    headers = response.headers
    print(f'headers: {headers}')
    
    loaded_background_json = json.loads(background_response.text)
    loaded_json = json.loads(response.text)
    #print(f"loaded_background_json: {loaded_background_json}")
    #print(f"loaded_background_json_url: {loaded_background_json['url']}")
    #print(f"loaded_json: {loaded_json}")
    background_src=loaded_background_json['url']
    rover_name = loaded_json['photos'][0]['rover']['name']
    launch_date = loaded_json['photos'][0]['rover']['launch_date']
    date_obj = datetime.strptime(launch_date, "%Y-%m-%d")
    launch_date = date_obj.strftime("%d/%m/%Y")
    landing_date = loaded_json['photos'][0]['rover']['landing_date']
    date_obj = datetime.strptime(landing_date, "%Y-%m-%d")
    landing_date = date_obj.strftime("%d/%m/%Y")
    max_sol = loaded_json['photos'][0]['rover']['max_sol']
    images_list = []
    for i in range(max_sol, max_sol - 6, -1):
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol={i}&page=1&api_key={settings.NASA_API_KEY}')   
        headers = response.headers     
        print(f'headers: {headers}')
        if response.status_code == 200:
            loaded_json = json.loads(response.text)
            print(f"loaded_jsonaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: {loaded_json}")
            
            if 'photos' in loaded_json and len(loaded_json['photos']) > 0:
                prima_immagine = loaded_json['photos'][0]
                img_src = prima_immagine['img_src']
                earth_date = prima_immagine['earth_date']
                date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
                earth_date = date_obj.strftime("%d/%m/%Y")
                sol = prima_immagine['sol']
                #img_src = loaded_json['photos'][0]['img_src']
                #earth_date = loaded_json['photos'][0]['earth_date']
                #date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
                #earth_date = date_obj.strftime("%d/%m/%Y")
                #sol = loaded_json['photos'][0]['sol']
                
                images_list.append({'img_src': img_src, 'earth_date': earth_date, 'sol': sol})
            
    

    

    context = {
        'images_list': images_list,
        'background_src':background_src,
        'rover_name': rover_name,
        'launch_date': launch_date,
        'landing_date': landing_date


    }

    return render(request, "mars_api/home.html", context)
