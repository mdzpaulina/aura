from kubernetes import client, config

def parse_cpu(cpu_str):
    """
    Converts K8s CPU format to millicores.
    '150m' -> 150, '3000000n' -> 3
    """
    if not cpu_str: return 0
    
    if cpu_str.endswith('m'):
        return int(cpu_str.replace('m', ''))
    elif cpu_str.endswith('n'):
        # Convert nanocores to millicores
        return int(cpu_str.replace('n', '')) // 1000000
    else:
        # If it comes in whole cores (e.g., '1')
        return int(cpu_str) * 1000

def parse_memory(mem_str):
    """
    Converts K8s memory format to Megabytes.
    '256Mi' -> 256.0, '500000Ki' -> 488.28
    """
    if not mem_str: return 0.0
    
    if mem_str.endswith('Mi'):
        return float(mem_str.replace('Mi', ''))
    elif mem_str.endswith('Ki'):
        return round(float(mem_str.replace('Ki', '')) / 1024, 2)
    elif mem_str.endswith('Gi'):
        return float(mem_str.replace('Gi', '')) * 1024
    else:
        # If it comes in plain bytes
        return round(float(mem_str) / (1024 * 1024), 2)
    
def get_cluster_metrics(namespace="default"):
    """
    Connects to the cluster and returns a clean dictionary with the current consumption.
    """
    # Loads the local kubeconfig (the same one your terminal uses to connect to OCI)
    try:
        config.load_kube_config()
    except Exception as e:
        print("Error loading Kubernetes configuration. Are you connected to the cluster?")
        return None

    api = client.CustomObjectsApi()
    clean_data = []

    try:
        # Query the Kubernetes Metrics Server
        metrics = api.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )

        for pod in metrics.get('items', []):
            pod_name = pod['metadata']['name']
            
            for container in pod['containers']:
                container_name = container['name']
                raw_cpu = container['usage']['cpu']
                raw_mem = container['usage']['memory']
                
                # Pass the data through our parsing functions
                clean_data.append({
                    "pod": pod_name,
                    "container": container_name,
                    "cpu_usage_millicores": parse_cpu(raw_cpu),
                    "memory_usage_mb": parse_memory(raw_mem)
                })

        return clean_data

    except Exception as e:
        print(f"Error getting metrics: {e}")
        print("Make sure the Metrics Server is installed in your OCI cluster.")
        return None

if __name__ == "__main__":
    metrics = get_cluster_metrics()
    if metrics:
        print("Clean metrics ready for the AI:")
        for m in metrics:
            print(m)