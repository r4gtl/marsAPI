from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from django.core.cache import cache
from django.http import JsonResponse

import requests
import json
import random

# Create your views here.


def get_images(request, rover_name, max_sol):
    print("Sono qui")
    # Ottieni un numero casuale nell'intervallo di sol desiderato
    #rover_name = request.GET.get('rover_name')
    print(f'rover_name= {rover_name}')
    print(f'max_sol: {max_sol}')
    #max_sol = int(request.GET.get('max_sol'))  # Assicurati di convertire max_sol in un intero
    print(f'max_sol: {max_sol}')
    random_sols = [random.randint(1, max_sol) for _ in range(3)]
    
    images_list = []
    data = {}  # Inizializza il dizionario data al di fuori del ciclo
    
    for i in random_sols:
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol={i}&page=1&api_key={settings.NASA_API_KEY}')   
        headers = response.headers     
        #print(f'headers: {headers}')
        if response.status_code == 200:
            loaded_json = json.loads(response.text)
            #print(f"loaded_jsonaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: {loaded_json}")
            
            if 'photos' in loaded_json and len(loaded_json['photos']) > 0:
                prima_immagine = loaded_json['photos'][0]
                img_src = prima_immagine['img_src']
                earth_date = prima_immagine['earth_date']
                date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
                earth_date = date_obj.strftime("%d/%m/%Y")
                sol = prima_immagine['sol']
                photo_id = loaded_json['photos'][0]['id']
                
                
                images_list.append({'img_src': img_src, 'earth_date': earth_date, 'sol': sol, 'photo_id': photo_id})
    print(f'images_list:  {images_list}')
    data = {'images_list': images_list}
    print(f'data: {data}')

    
    return JsonResponse(data, safe=False)





def home(request, rover_name='curiosity'):

    print('rover_name: {rover_name}' )
    #latest_response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={settings.NASA_API_KEY}')
    background_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={settings.NASA_API_KEY}')
    #response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol=100&page=1&api_key={settings.NASA_API_KEY}')
    response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/latest_photos?api_key={settings.NASA_API_KEY}')
    #all_images_response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?api_key={settings.NASA_API_KEY}')
    #print(f'all_images_response.status_code: {all_images_response.status_code}')
    headers = response.headers
    #print(f'headers: {headers}')
    #print(f'latest_response: {latest_response}')
    
    loaded_background_json = json.loads(background_response.text)
    loaded_json = json.loads(response.text)
    #loaded_all_images_response = json.loads(all_images_response.text)

    #print(f'loaded_all_images_response: {loaded_all_images_response}')


    #loaded_latest_response = json.loads(latest_response.text)
    #print(f"loaded_background_json: {loaded_background_json}")
    #print(f"loaded_background_json_url: {loaded_background_json['url']}")
    #print(f"loaded_json: {loaded_json}")

    #print(f'loaded_latest_response: {loaded_latest_response}')
    background_src=loaded_background_json['url']
    rover_name = loaded_json['latest_photos'][0]['rover']['name']
    launch_date = loaded_json['latest_photos'][0]['rover']['launch_date']
    date_obj = datetime.strptime(launch_date, "%Y-%m-%d")
    launch_date = date_obj.strftime("%d/%m/%Y")
    landing_date = loaded_json['latest_photos'][0]['rover']['landing_date']
    date_obj = datetime.strptime(landing_date, "%Y-%m-%d")
    landing_date = date_obj.strftime("%d/%m/%Y")
    max_sol = loaded_json['latest_photos'][0]['rover']['max_sol']
    images_list = []
    for i in range(max_sol, max_sol - 3, -1):
        response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol={i}&page=1&api_key={settings.NASA_API_KEY}')   
        
        
        if response.status_code == 200:
            loaded_json = json.loads(response.text)
            #print(f"loaded_jsonaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: {loaded_json}")
            
            if 'photos' in loaded_json and len(loaded_json['photos']) > 0:
                prima_immagine = loaded_json['photos'][0]
                img_src = prima_immagine['img_src']
                earth_date = prima_immagine['earth_date']
                date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
                earth_date = date_obj.strftime("%d/%m/%Y")
                sol = prima_immagine['sol']
                photo_id = loaded_json['photos'][0]['id']
                #print(f'photo_id: {photo_id}')
                
                
                images_list.append({'img_src': img_src, 'earth_date': earth_date, 'sol': sol, 'photo_id': photo_id})

            print(f"max_sol: {max_sol}")
  
    context = {
        'images_list': images_list,
        'background_src':background_src,
        'rover_name': rover_name,
        'launch_date': launch_date,
        'landing_date': landing_date,
        'max_sol': max_sol
        


    }

    return render(request, "mars_api/home.html", context)
