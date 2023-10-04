import pandas as pd
import numpy as np
import re
from transformers import T5Tokenizer, T5EncoderModel
import torch

# Function to process sequences and generate embeddings
def process_sequences(sequences):
    sequences = [" ".join(list(re.sub(r"[UZOB]", "X", sequence))) for sequence in sequences]
    sequences = ["<AA2fold>" + " " + s for s in sequences]
    ids = tokenizer.batch_encode_plus(sequences, add_special_tokens=True, padding="longest", return_tensors='pt').to(device)
    with torch.no_grad():
        embedding_repr = model(ids.input_ids, attention_mask=ids.attention_mask)
    embeddings = [emb.mean(dim=0).cpu().numpy() for emb in embedding_repr.last_hidden_state]
    return embeddings

# Load the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('Rostlab/ProstT5', do_lower_case=False)
model = T5EncoderModel.from_pretrained("Rostlab/ProstT5")
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Load preprocessed training data
train_data_path = 'Train_lact/lact.csv'
train_data = pd.read_csv(train_data_path)

# Extract unique pairs of UniProt IDs and sequences and filter by length
unique_pairs_df = train_data[['EntryID', 'Sequence']].drop_duplicates()
unique_pairs_df = unique_pairs_df[unique_pairs_df['Sequence'].str.len() <= 6500]  # Filter by length
unique_sequences = unique_pairs_df['Sequence'].tolist()
unique_uniprot_ids = unique_pairs_df['EntryID'].tolist()

# Process unique pairs in batches
batch_size = 1
embeddings_file = 'Train_lact/embeddings.npy'
uniprot_ids_file = 'Train_lact/uniprot_ids_pairs.csv'
embeddings_list = []

for i in range(0, len(unique_sequences), batch_size):
    print(f"Processing batch {i // batch_size + 1}...")
    print(f"Processing UniProtIDs: {', '.join(unique_uniprot_ids[i:i + batch_size])}")
    sequences_batch = unique_sequences[i:i + batch_size]
    embeddings_batch = process_sequences(sequences_batch)
    embeddings_list.extend(embeddings_batch)

# Convert to NumPy array and save to .npy file
np.save(embeddings_file, np.array(embeddings_list))

# Save UniProtID-sequence pairs to a text file
unique_pairs_df.to_csv(uniprot_ids_file, index=False)

print("Embedding generation completed! Embeddings saved to 'Train/embeddings.npy'")
