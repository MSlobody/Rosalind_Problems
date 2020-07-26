import re

# Convert FASTA file to list of DNA sequences
def FASTA_to_list(file):
    file_info = ""
    handle = open(file)
    for line in handle:
        file_info += line.strip()
    file_list = file_info.split(">")

    ID_DNAseq = []
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
        nuc_seq = entry[1]
        for i in data:
            ID_=i[0]
            nuc_seqq =i[1]
            if nuc_seq == nuc_seqq:
                continue
            elif nuc_seq[-k:] == nuc_seqq[:k]:
                print(ID,ID_)
                adj_IDs.append((ID,ID_))
    return adj_IDs

adj_IDs = adjacency_list('Sample_data',3)








