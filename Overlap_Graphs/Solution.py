import re

# Convert FASTA file to list of IDs and DNA sequences
def FASTA_to_list(file):
    file_info = ""
    ID_DNAseq = []
    handle = open(file)

    for line in handle:
        file_info += line.strip()
    file_list = file_info.split(">")

    for entry in file_list:
        if len(entry) <= 2:
            continue
        DNA_seq = re.findall("[ATCG]+",entry)
        ID = entry[:-(len(DNA_seq[0]))]
        ID_DNAseq.append([ID,DNA_seq[0]])
    return ID_DNAseq

# Creates a list of all the FASTA sequences whose suffix matches the prefix of another sequence of length k.
def adjacency_list(file,k):
    data = FASTA_to_list(file)
    adj_IDs = []

    for entry in data:
        ID = entry[0]
        nuc_seq_prefix = entry[1]
        for i in data:
            ID_=i[0]
            nuc_seq_suffix =i[1]
            if nuc_seq_prefix == nuc_seq_suffix:
                continue
            elif nuc_seq_prefix[-k:] == nuc_seq_suffix[:k]:
                print(ID,ID_)
                adj_IDs.append((ID,ID_))
    return adj_IDs

matches = adjacency_list('Sample_data',3)
print(matches)
