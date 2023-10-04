from Bio import SeqIO
import csv

# input multifasta file
input_fasta_file = "./Train_lact/all_lact.fas"

# output csv file with 2 columns will be generated
output_csv_file = "./Train_lact/lact.csv"

with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # header 
    csv_writer.writerow(['EntryID', 'Sequence'])
    
    # parse
    for record in SeqIO.parse(input_fasta_file, "fasta"):
        entry_id = record.id
        sequence = str(record.seq)
        
       
        csv_writer.writerow([entry_id, sequence])

print(f"CSV file '{output_csv_file}' has been created successfully.")
