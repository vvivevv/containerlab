#purpose of this python file is to create a yaml which is used as an input into containerlabs to create fabric
# this code will generate a 3 stage clos fabric yaml with a few user inputs which can then be deployed via container labs

import json

def generate_yaml(filename, name, spine_count, leaf_count, image_version):
    data = {
        "name": name,
        "topology": {
            "nodes": {},
            "links": []
        }
    }

    # Create nodes
    for i in range(1, spine_count + 1):
        data["topology"]["nodes"][f"spine{i}"] = {
            "kind": "nokia_srlinux",
            "image": f"ghcr.io/nokia/srlinux:{image_version}"
        }

    for i in range(1, leaf_count + 1):
        data["topology"]["nodes"][f"leaf{i}"] = {
            "kind": "nokia_srlinux",
            "image": f"ghcr.io/nokia/srlinux:{image_version}"
        }

    # Create links
    for i in range(1, leaf_count + 1):
        for j in range(1, spine_count + 1):
            data["topology"]["links"].append({
                "endpoints": [f"spine{j}:e1-{i}", f"leaf{i}:e1-{j}"]
            })

    # Convert to YAML
    yaml_output = ""
    yaml_output += f"name: {name}\n\n"
    yaml_output += "topology:\n"
    yaml_output += "  nodes:\n"
    for node, details in data["topology"]["nodes"].items():
        yaml_output += f"    {node}:\n"
        yaml_output += f"      kind: {details['kind']}\n"
        yaml_output += f"      image: {details['image']}\n"

    yaml_output += "\n  links:\n"
    for link in data["topology"]["links"]:
        yaml_output += f"  - endpoints: {json.dumps(link['endpoints'])}\n"

    # Write to file
    with open(filename, 'w') as file:
        file.write(yaml_output)

    print(f"YAML file generated: {filename}")


def main():
    name = input("Enter the name (default: srl3stage01): ")
    name = name.strip() or "srl3stage01"

    image_version = input("Enter the image version (default: 24.3.3): ")
    image_version = image_version.strip() or "24.3.3"

    while True:
        try:
            spine_count = int(input("Enter the number of spine nodes: "))
            leaf_count = int(input("Enter the number of leaf nodes: "))
            break
        except ValueError:
            print("Invalid input. Please enter integers.")

    filename = f"{name}.yaml"
    generate_yaml(filename, name, spine_count, leaf_count, image_version)


if __name__ == "__main__":
    main()
