import base64
import json
from django.shortcuts import render


def show_map(request):
    with open('clustering/data.json') as f:
        clusters = json.load(f)
    imgs = []
    data = []
    lat = []
    lon = []
    for cluster in clusters:
        with open(cluster['figure_path'], 'rb') as f:
            imgs.append(base64.b64encode(f.read()).decode('utf-8'))
        data.append(cluster['data'])
        lat.append(cluster['latitude'])
        lon.append(cluster['longitude'])
    data = {
        'lat': json.dumps(lat),
        'lon': json.dumps(lon),
        'imgs': json.dumps(imgs),
        'text': json.dumps(list(range(len(lat)))),
        'lat_center': sum(lat) / len(lat),
        'lon_center': sum(lon) / len(lon)
    }
    return render(request, 'clustering/show_map.html', data)
