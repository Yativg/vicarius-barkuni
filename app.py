import json
from flask import Flask, render_template, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = Flask(__name__)

def get_kube_config():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("Could not configure Kubernetes Python client")
    v1 = client.CoreV1Api()
    return v1

def get_pod_status(pod):
    status = pod['status']['phase']
    for container_status in pod['status'].get('containerStatuses', []):
        if not container_status.get('started', True) or not container_status.get('ready', True):
            waiting_state = container_status['state'].get('waiting')
            if waiting_state:
                status = waiting_state.get('reason', status)
    return status

def get_pods_in_kube_system():
    v1 = get_kube_config()
    try:
        raw_pods = v1.list_namespaced_pod(namespace="kube-system", _preload_content=False)
        pods = json.loads(raw_pods.data)
        pods_details_list = []

        for pod in pods['items']:
            conditions = [
                cond for cond in pod['status'].get('conditions', [])
                if cond['type'] in ['ContainersReady', 'Initialized', 'PodScheduled', 'Ready']
            ]
            pod_status = get_pod_status(pod)
            pod_dict = {
                "name": pod['metadata']['name'],
                "namespace": pod['metadata']['namespace'],
                "ip": pod['status'].get('podIP'),
                "node": pod['spec'].get('nodeName'),
                "status": pod_status,
                "conditions": conditions
            }
            pods_details_list.append(pod_dict)

        return pods_details_list
    except ApiException as e:
        print("Error accessing Kubernetes API:", e)
        return []

@app.route('/')
def welcome():
    return "Welcome to Barkuni Corp!"

@app.route('/pods')
def pods():
    pods_list = get_pods_in_kube_system()
    return render_template('pods.html', pods_list=pods_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)