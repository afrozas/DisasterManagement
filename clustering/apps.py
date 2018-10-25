import subprocess
import sys
import os
from django.apps import AppConfig
import threading
from DisasterManagement.settings import BASE_DIR, CLUSTER_RUN_INTERVAL


def run_plotting_script():
    script_path = os.path.join(BASE_DIR, 'clustering/plotting_script.py')
    subprocess.Popen([sys.executable, script_path])
    threading.Timer(CLUSTER_RUN_INTERVAL, run_plotting_script).start()


class ClusteringConfig(AppConfig):
    name = 'clustering'

    def ready(self):
        run_plotting_script()
