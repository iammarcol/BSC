# BSC
Repository created for projects done at BSC 2023/24

-> In the directory /ProstT5 a python script for creating sequence embeddings "generate_emb.py" can be found. It is used to create sequence embeddings based on a multifasta imput file. The input file has to be in csv format and contain a header with EntryID and Sequence as columns at least. It can also contain other columns, if needed. The example csv file can be found at /Train/all_globins.csv. Along with this file, the original multifasta file with globin sequences is also provided, along with an additional python script "csv_generate.py" which is used to convert multifasta file to csv format. 

-> Embeddings script asks for the input path and it generates two output files which paths are to be modified inside of the script:

train_data_path = 'Train/input.csv'
embeddings_file = 'Train/embeddings.npy'
uniprot_ids_file = 'Train/uniprot_ids_pairs.csv'

-> The commandline for the scrip execution is: 

$ python generate_emb.py 

-> Once the output embeddings file "embeddings.npy" is created, in the same directory you can find a python notebook file "emb_plotting.ipynb" which is used to visualize the embeddings. Mofifications can be made in the code in order to color the embeddings differently. In the given example, they are colored based on their IDs in order to differentiate between different globin groups. The plot is interactive.

-> Plotting the reduced embeddings should output a similar plot as this one:

![Alt Text](https://github.com/yourusername/yourrepository/raw/main/images/example.png)






