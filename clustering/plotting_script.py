import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import random
import os
import json
import sys

ROOT_DIR = '' if len(sys.argv) < 2 else sys.argv[1]

FIGURE_DIR = os.path.join(ROOT_DIR, 'plot_figures')


def create_cluster_json(cluster_dict):
    cluster_json = {}
    for key in cluster_dict:
        cluster_json[str(key)] = cluster_dict[key]
    return cluster_json


def empty_figure_folder(folder=FIGURE_DIR):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def load_data(file_name):
    df = pd.read_csv(file_name)
    return df


def geo_clustering(df):
    lat, lng = df['latitude'], df['longitude']
    kmeans = KMeans(n_clusters=11)
    kmeans.fit(list(zip(lat, lng)))
    centers = np.array(kmeans.cluster_centers_)
    labels = kmeans.labels_
    plt.scatter(lat, lng, c=labels)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1])
    return centers, labels


def center_based_list(centers, labels, df):
    lat, lng, keywords = df['latitude'], df['longitude'], df['keyword']
    dick = {}
    for idx, cen in enumerate(labels):
        location = {}
        location['lat'] = lat[idx]
        location['log'] = lng[idx]
        location['keywords'] = keywords[idx]
        if cen in dick:
            dick[cen].append(location)
        else:
            dick[cen] = []
            dick[cen].append(location)

    location_stats = {}
    keyword_stats = {}
    for label in dick:
        cluster_list = dick[label]
        cluster_stats = {}
        for item in cluster_list:
            words = item['keywords'].split(',')
            for word in words:
                if word not in ["Food", "Water", "Medicines", "Clothing", "Appliances", "Others"]:
                    word = "Others"
                if word not in cluster_stats:
                    cluster_stats[word] = 1
                else:
                    cluster_stats[word] += 1

                if word not in keyword_stats:
                    keyword_stats[word] = 1
                else:
                    keyword_stats[word] += 1

            location_stats[label] = cluster_stats

    return dick, location_stats, keyword_stats


def plot_top_location_stats(centers, location_stats, all_points_json, top_n=5):
    base_colors = "grcmyb"
    plot_data_json = []

    # _ is cluster centers
    for _ in location_stats:
        individual_cluster_json = {}
        sizes = []
        labels = []
        clustered_location_stats = location_stats[_]
        total_counts = 0
        for key in clustered_location_stats:
            sizes.append(clustered_location_stats[key])
            total_counts += clustered_location_stats[key]
            labels.append(key)

        for idx in range(0, len(labels)):
            labels[idx] += f" {round((sizes[idx]/total_counts)*100, 2)}%"

        lat, lng = centers[_]
        figure_name = "{}_{}.png".format(lat, lng)
        figure_path = os.path.join(FIGURE_DIR, figure_name)
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        explode_split = random.randint(1, top_n)
        explode = (0.1,) * explode_split + (0.0,) * (top_n - explode_split)
        colors = ''.join(random.sample(base_colors, len(base_colors)))
        wedges, texts = ax.pie(
            sizes, wedgeprops=dict(width=0.5), startangle=-40)
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)

        # plt.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=100)
        plt.axis('equal')
        fig.savefig(figure_path)

        individual_cluster_json['figure_path'] = figure_path
        individual_cluster_json['data'] = clustered_location_stats
        individual_cluster_json['latitude'] = lat
        individual_cluster_json['longitude'] = lng
        individual_cluster_json['points'] = all_points_json[str(_)]

        plot_data_json.append(individual_cluster_json)

    return plot_data_json


def plot(file_name=os.path.join(ROOT_DIR, 'large_set.csv')):
    empty_figure_folder()
    df = load_data(file_name)
    centers, labels = geo_clustering(df)
    dick, location_stats, keyword_stats = center_based_list(
        centers, labels, df)
    all_points_json = create_cluster_json(dick)
    clustering_data = plot_top_location_stats(centers, location_stats, all_points_json)
    with open(os.path.join(ROOT_DIR, 'data.json'), 'w') as fp:
        json.dump(clustering_data, fp, indent=4)
    with open(os.path.join(ROOT_DIR, 'all_points.json'), 'w') as fp:
        json.dump(all_points_json, fp, indent=4)


plot()
