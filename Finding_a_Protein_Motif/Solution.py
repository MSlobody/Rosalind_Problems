from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Convert IDs from text file to uniprot links
def file_to_list(file):
    handle = open(file)
    uniprot_links = []
    uniprot_IDs = []
    for line in handle:
        line_info = "https://www.uniprot.org/uniprot/" + line.strip()
        uniprot_links.append(line_info)
        uniprot_IDs.append(line.strip())
    return uniprot_links, uniprot_IDs

uniprot_links = file_to_list('Sample_data')[0]
uniprot_IDs = file_to_list('Sample_data')[1]

# Search each link and parse the HTML file with beautifulsoup to obtain the <pre> tags where the amino acid sequences are stored.
# Retain only the amino acid sequences and ID of each protein from the <pre> tag
proteins = []
for ID, link in zip(uniprot_IDs,uniprot_links):
    html = urlopen(link, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('pre')
    str_tags = ''
    protein_seq = ""
    # Convert <pre> tags to a larger string.
    for tag in tags:
        str_tags += str(tag)
    # Retain only the amino acid sequence of the protein, removing all other tag info and metadata.
    a_a_seqs = re.findall('[ARNDCEQGHILKMFPSTWYV]+',str_tags)
    for seq in a_a_seqs:
        if len(seq) <= 11:
            continue
        else:
            protein_seq += seq
    proteins.append([ID,protein_seq])
#print(proteins)

# Identify the starting location(s) of the N{P}[ST]{P} motif in the protein sequences.
locals = []
for i in proteins:
    protein = i[1]
    for k in range(len(protein)-3):
        if protein[k] == "N" and protein[k+1] != "P" and (protein[k+2] == "S" or protein[k+2] == "T") and protein[k+3] != "P":
            locals.append(k+1)
    if len(locals) > 0:
        print(i[0])
        print(" ".join([str(j) for j in locals]))
    locals = []