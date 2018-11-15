import base64
import json
from collections import defaultdict
from django.shortcuts import render


def read_cluster_data():
    with open('clustering/data.json') as f:
        clusters = json.load(f)
    cluster_centers = defaultdict(list)
    all_points_data = {}
    for index, cluster in enumerate(clusters):
        try:
            with open(cluster['figure_path'], 'rb') as f:
                cluster_centers['imgs'].append(
                    base64.b64encode(f.read()).decode('utf-8'))
        except FileNotFoundError:
            print("SDSDFSDFSDF")
            cluster_centers['imgs'].append(None)
        cluster_centers['lat'].append(cluster['latitude'])
        cluster_centers['lon'].append(cluster['longitude'])
        lat, lon, text = [], [], []
        for point in cluster['points']:
            lat.append(point['lat'])
            lon.append(point['log'])
            text.append(point['keywords'])
        all_points_data[index] = {'lat': json.dumps(
            lat), 'lon': json.dumps(lon), 'text': json.dumps(text)}
    return cluster_centers, all_points_data


def show_map(request):
    centers, all_points = read_cluster_data()
    lat, lon = centers['lat'], centers['lon']

    data = {
        'centers': {
            'lat': lat,
            'lon': lon,
            'imgs': json.dumps(centers['imgs']),
            'text': json.dumps([f'Cluster {i}' for i in range(1, len(lat) + 1)]),
            'lat_center': sum(lat) / len(lat),
            'lon_center': sum(lon) / len(lon)
        },
        'all': all_points
    }
    return render(request, 'clustering/show_map.html', data)
