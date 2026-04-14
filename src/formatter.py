import yaml
import os

def save_optimized_yaml(recommendations_json, file_path="optimized-resources.yaml"):
    """
    Takes the AURA JSON and generates a YAML file with the resource blocks 
    ready to be copied or applied to Kubernetes manifests.
    """
    if not recommendations_json or "recommendations" not in recommendations_json:
        print("No valid recommendations received from the AI.")
        return False

    yaml_documents = []
    
    # Iterate over each recommendation made by the AI
    for rec in recommendations_json["recommendations"]:
        container = rec.get("container", "unknown")
        cpu = rec.get("new_cpu_limit", 100)
        memory = rec.get("new_memory_limit_mb", 128)
        reasoning = rec.get("reasoning", "")
        
        # Structure the standard Kubernetes format for 'resources'
        resource_block = {
            "_ai_comment": f"AURA adjusted {container} -> {reasoning}",
            "name": container,
            "resources": {
                "requests": {
                    "memory": f"{memory}Mi",
                    "cpu": f"{cpu}m"
                },
                "limits": {
                    "memory": f"{memory}Mi",
                    "cpu": f"{cpu}m"
                }
            }
        }
        yaml_documents.append(resource_block)

    try:
        # Write the file to disk
        with open(file_path, 'w') as file:
            # Add a header for the team
            file.write("# Auto-generated file by AURA (Adaptive Usage and Resource Agent)\n")
            file.write("# Review the limits before applying with kubectl.\n\n")
            
            yaml.dump_all(yaml_documents, file, default_flow_style=False, sort_keys=False)
            
        return True
    
    except Exception as e:
        print(f"Error writing the YAML file: {e}")
        return False