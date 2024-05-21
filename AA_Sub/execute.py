import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from Bio import SeqIO

# Argument parsing
parser = argparse.ArgumentParser(description='Process sequence and trajectory data.')
parser.add_argument('sequence_fasta_file', type=str, help='Path to the sequence FASTA file.')
parser.add_argument('trajectories_file', type=str, help='Path to the trajectories CSV file.')
parser.add_argument('df_colores_file', type=str, help='Path to the DF_Colores CSV file.')
parser.add_argument('save_directory', type=str, help='Directory to save the plots.')

args = parser.parse_args()

# Read trajectories.csv and extract the Trajectory column
trajectories_df = pd.read_csv(args.trajectories_file)
trajectories = {}
for idx, row in trajectories_df.iterrows():
    node = row['Node']
    trajectory = row['Trajectory'].split(', ')
    trajectories[node] = trajectory

# Read sequences from the provided FASTA file and filter based on protein names
sequences = {}
with open(args.sequence_fasta_file, 'r') as fasta_file:
    for record in SeqIO.parse(fasta_file, 'fasta'):
        sequences[record.id] = record.seq

# Read DF_Colores CSV file
DF_Colores = pd.read_csv(args.df_colores_file)

# Create a dictionary to store FstState values for each (PDBID, pos) pair
fst_states = {}
for idx, row in DF_Colores.iterrows():
    pdb_id = row['PDBID']
    pos = row['pos']
    fst_state = row['FstState']
    fst_states[(pdb_id, pos)] = fst_state

# Create directory to save trajectory plots if it doesn't exist
save_dir = args.save_directory
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Get FstState values for node_76
node76_fst_states = {}
for pos, state in zip(DF_Colores['pos'], DF_Colores['FstState']):
    node76_fst_states[pos] = state

# Iterate through each trajectory
for node, protein_names in trajectories.items():
    # Retrieve the last instance in protein_names list as trajectory name
    trajectory_name = protein_names[-1]

    # Output the trajectory name
    print()
    print(f"Trajectory: {trajectory_name}")

    # Create lists to store data for plotting
    positions = []
    protein_names_plot = []
    changes = []

    # Define specified positions and additional residue positions
    specified_position = [209]
    additional_positions = [102,143,190,195,209,212,219,220,221]

    # Get the set of protein names for the current trajectory
    protein_names_in_trajectory = set(protein_names)

    # Iterate through consecutive pairs of sequences within the trajectory
    for i in range(len(protein_names) - 1):
        seq1_name = protein_names[i]
        seq2_name = protein_names[i + 1]

        # Retrieve sequences for comparison
        seq1 = sequences.get(seq1_name)
        seq2 = sequences.get(seq2_name)

        if seq1 and seq2:
            for index, (aa1, aa2) in enumerate(zip(seq1, seq2), start=1):
                # Store data for changes at additional positions
                if index in additional_positions and aa1 != aa2:
                    positions.append(index)
                    protein_names_plot.append(seq2_name)  # Use seq2_name for the color assignment
                    changes.append(f"{aa1}{index}{aa2}")

    # Plot amino acid changes only if there are changes at additional positions
    if positions:
        plt.figure(figsize=(13, 6))  # Adjust figure size

        # Get corresponding FstState for specified position and assign color to the reference line
        specified_position_fst_state = fst_states.get(('node_76', specified_position[0]), None)
        if specified_position_fst_state == 'MIN':
            specified_position_color = 'green'
        elif specified_position_fst_state == 'NEU':
            specified_position_color = 'grey'
        elif specified_position_fst_state == 'MAX':
            specified_position_color = 'red'
        else:
            specified_position_color = 'black'  # Default color

        # Plot reference line for specified position
        plt.axvline(x=specified_position[0], color=specified_position_color, linestyle='--',
                    label=f'CS {specified_position[0]}')

        # Get corresponding FstState for each position and assign color based on aa2 (seq2_name)
        additional_positions_colors = []
        additional_aa_labels_colors = []  # Color for amino acid labels on x-axis
        for pos, protein_name in zip(positions, protein_names_plot):
            fst_state = fst_states.get((protein_name, pos), None)
            if fst_state == 'MIN':
                color = 'green'
            elif fst_state == 'NEU':
                color = 'grey'
            elif fst_state == 'MAX':
                color = 'red'
            else:
                color = 'black'  # Default color
            additional_positions_colors.append(color)
            
            # Get the FstState for the position from node_76
            specified_position_fst_state = fst_states.get(('node_76', specified_position[0]), None)
            node76_fst_state = fst_states.get(('node_76', additional_positions[0]), None)
            if node76_fst_state == 'MIN':
                aa_label_color = 'green'
            elif node76_fst_state == 'NEU':
                aa_label_color = 'grey'
            elif node76_fst_state == 'MAX':
                aa_label_color = 'red'
            else:
                aa_label_color = 'black'  # Default color
            additional_aa_labels_colors.append(aa_label_color)

        # Get the FstState for each position from node_76
        node76_fst_states = {}
        for pos in additional_positions:
            node76_fst_state = fst_states.get(('node_76', pos), None)
            node76_fst_states[pos] = node76_fst_state

        # Now, for each position, determine the color of the label based on its FstState from node_76
        additional_aa_labels_colors = []
        for pos in additional_positions:
            node76_fst_state = node76_fst_states.get(pos)
            if node76_fst_state == 'MIN':
                aa_label_color = 'green'
            elif node76_fst_state == 'NEU':
                aa_label_color = 'grey'
            elif node76_fst_state == 'MAX':
                aa_label_color = 'red'
            else:
                aa_label_color = 'black'  # Default color
            additional_aa_labels_colors.append(aa_label_color)

        last_protein_name = protein_names[-1]
        last_protein_fst_states = {}
        for pos in additional_positions:
            last_protein_fst_state = fst_states.get((last_protein_name, pos), None)
            last_protein_fst_states[pos] = last_protein_fst_state

        additional_aa_labels_colors_lp = []
        for pos in additional_positions:
            last_protein_fst_state = last_protein_fst_states.get(pos)
            if last_protein_fst_state == 'MIN':
                aa_label_color = 'green'
            elif last_protein_fst_state == 'NEU':
                aa_label_color = 'grey'
            elif last_protein_fst_state == 'MAX':
                aa_label_color = 'red'
            else:
                aa_label_color = 'black'  # Default color
            additional_aa_labels_colors_lp.append(aa_label_color)

        # Plot all positions changes
        plt.scatter(positions, [protein_names.index(p) for p in protein_names_plot], marker='o',
                    c=additional_positions_colors, label='AA change')

        # Get node_76 sequence
        node_76_aa_sequence = sequences.get('node_76')
        if node_76_aa_sequence:
            # Set x-axis ticks with amino acids from node_76 for additional positions
            ax = plt.gca()
            ax.set_xticks(additional_positions)
            # Set x-axis tick labels based on node_76 amino acid sequence
            xtick_labels = []
            for pos in additional_positions:
                if 0 <= pos - 1 < len(node_76_aa_sequence):
                    xtick_labels.append(node_76_aa_sequence[pos - 1])
                else:
                    xtick_labels.append('')  # If index is out of range, set label to empty string
            ax.set_xticklabels(xtick_labels)
            for label, color in zip(ax.get_xticklabels(), additional_aa_labels_colors):
                label.set_color(color)
        else:
            print("node_76 sequence not found.")

        # if we want it to be from 0 to the last position in the seq 
        # node76_sequence_length = len(sequences.get('node_76', ''))
        last_it = additional_positions[-1]
        item = last_it + 4
        ax.set_xlim([30, item])

        last_protein_name = protein_names[-1]
        last_protein_sequence = sequences.get(last_protein_name)
        last_protein_fst_states = {pos: fst_states.get((last_protein_name, pos)) for pos in additional_positions}
        if last_protein_sequence:
            ax2 = ax.twiny()
            ax2.set_xlim(ax.get_xlim())
            ax2.set_xticks(additional_positions)
            xtick_labels_last_protein = [last_protein_sequence[pos - 1] if 0 <= pos - 1 < len(last_protein_sequence) else '' for pos in additional_positions]
            ax2.set_xticklabels(xtick_labels_last_protein)
            for label, color in zip(ax2.get_xticklabels(), additional_aa_labels_colors_lp):
                label.set_color(color)
        else:
            print("Last protein sequence not found.")

        plt.yticks(range(len(protein_names)), protein_names)  # Set y-axis ticks and labels for this trajectory only
        plt.xlabel('Position / Amino Acids')
        plt.ylabel('Protein Names')
        plt.title(f'Amino Acid Changes for Trajectory: {trajectory_name}')
        for i, txt in enumerate(changes):
            plt.annotate(txt, (positions[i], protein_names.index(protein_names_plot[i])), textcoords="offset points",
                         xytext=(0, 5), fontsize=8, ha='center')
        plt.grid(True)
        plt.legend()

        # Save plot
        plt.savefig(os.path.join(save_dir, f"trajectory_{trajectory_name}.png"))
        plt.close()
    else:
        print("No amino acid changes found for this trajectory.")
