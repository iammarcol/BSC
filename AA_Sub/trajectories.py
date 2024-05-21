# based on the input phylogenetic tree in newick format, creates the output file with trajectories extrated from the tree
# it consists of names (fasta_IDs) of the proteins that are a part of each of the trajectories

from Bio import Phylo
import csv

# Replace 'your_tree.nex' with the path to your Nexus file
nexus_file = 'anc_new'

# Parse the Nexus tree
tree = Phylo.read(nexus_file, 'newick')

# Create a dictionary to store trajectories
trajectories = {}

# Define a function to recursively traverse the tree and build trajectories
def build_trajectories(clade, path=None):
    if path is None:
        path = []
    name = clade.name if clade.name else f'Unnamed_{unnamed_node_counter["count"]}'
    path.append(name)
    if clade.is_terminal():
        trajectories[name] = path[1:].copy()  # Exclude the first "Unnamed_1"
    for child in clade.clades:
        build_trajectories(child, path.copy())
    path.pop()

# Initialize a dictionary to hold the unnamed node counter
unnamed_node_counter = {'count': 1}

# Traverse the tree, assign labels to unnamed nodes, and build trajectories
build_trajectories(tree.root)

# Create a CSV file
csv_file = 'trajectories_novo.csv'

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Leaf Name', 'Trajectory'])

    for label, trajectory in trajectories.items():
        writer.writerow([label, ', '.join(trajectory)])

print(f"CSV file '{csv_file}' has been created.")
