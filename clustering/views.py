import base64
import json
from django.shortcuts import render


def read_cluster_center_data():
    with open('clustering/data.json') as f:
        clusters = json.load(f)
    imgs = []
    data = []
    lat = []
    lon = []
    for cluster in clusters:
        try:
            with open(cluster['figure_path'], 'rb') as f:
                imgs.append(base64.b64encode(f.read()).decode('utf-8'))
        except FileNotFoundError:
            imgs.append('')
        data.append(cluster['data'])
        lat.append(cluster['latitude'])
        lon.append(cluster['longitude'])
    return imgs, data, lat, lon


def read_all_points_data():
    with open('clustering/all_points.json') as f:
        all_points = json.load(f)
    data = {}
    for num, points in sorted(all_points.items(), key=lambda x: int(x[0])):
        lat = []
        lon = []
        keywords = []
        for point in points:
            lat.append(point['lat'])
            lon.append(point['log'])
            keywords.append(point['keywords'])
        data[num] = {'lat': json.dumps(
            lat), 'lon': json.dumps(lon), 'text': json.dumps(keywords)}
    return data


def show_map(request):
    imgs, _, lat, lon = read_cluster_center_data()
    data = {
        'centers': {
            'lat': lat,
            'lon': lon,
            'imgs': json.dumps(imgs),
            'text': json.dumps([f'Cluster {i}' for i in range(1, len(lat) + 1)]),
            'lat_center': sum(lat) / len(lat),
            'lon_center': sum(lon) / len(lon)
        },
        'all': read_all_points_data()
    }
    return render(request, 'clustering/show_map.html', data)
