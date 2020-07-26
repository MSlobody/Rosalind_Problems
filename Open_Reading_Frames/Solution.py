import re
from data_structures import *

# Convert FASTA file to list of DNA sequence
def FASTA_to_list(file = "Sample_data"):
    file_info = ""
    handle = open(file)
    for line in handle:
        file_info += line.strip()
    file_list = file_info.split(">")

    for entry in file_list:
        if len(entry) <= 2:
            continue
        DNA_seq = re.findall("[ATCG]+",entry)
        return DNA_seq[0]

DNA_seq = FASTA_to_list()

# Obtains the reverse complement DNA strand (5' to 3' direction) and converts both strands to an RNA sequence.
def RNA_strands():
    data = DNA_seq
    sense_strand = ""
    antisense_strand = ""
    for nuc in data:
        if nuc == "T":
            sense_strand += "U"
            antisense_strand += rev_dict["T"]
        elif nuc == "A":
            sense_strand += "A"
            antisense_strand += "U"
        else:
            sense_strand += nuc
            antisense_strand += rev_dict[nuc]

    return [sense_strand, antisense_strand[::-1]]

# Translates both RNA sequence strands with 3 reading frames each returning all 6 translated sequences.
def translation():
    data = RNA_strands()
    f1,r1,f2,r2,f3,r3 = "","","","","",""

    for i in range(0,len(data[0])-2,3):
        f1 += RNA_Cod[data[0][i:i+3]]
        r1 += RNA_Cod[data[1][i:i+3]]


    for i in range(1,len(data[0])-2,3):
        f2 += RNA_Cod[data[0][i:i + 3]]
        r2 += RNA_Cod[data[1][i:i + 3]]

    for i in range(2, len(data[0])-2,3):
        f3 += RNA_Cod[data[0][i:i + 3]]
        r3 += RNA_Cod[data[1][i:i + 3]]

    return [f1,f2,f3], [r1,r2,r3]

# Identifies all the open reading frames for the forward or reverse strands. x = 0 fwd strand translated transcripts, x = 1 rev strand translated transcripts
def ORF(x):
    f = translation()[x]
    ORFs = []
    count = 0
    protein = ""

    for seq in f:
        for amino_a in seq:
            count += 1
            if amino_a == "M":
                for i in range(count-1,len(seq)):
                    if seq[i] == "_":
                        ORFs.append(protein)
                        break
                    protein += seq[i]
                protein = ""
        count = 0
    return ORFs

# Combines all open reading frames from fwd and rev strands and identifies unique peptides to print.
all_ORFs = ORF(0) + ORF(1)
all_unique_ORFs = list(set(all_ORFs))

for entry in all_unique_ORFs:
    print(entry)