import re

# Convert FASTA file to list of DNA sequences
def FASTA_to_list(file):
    file_info = ""
    handle = open(file)
    for line in handle:
        file_info += line.strip()
    file_list = file_info.split(">")

    DNA_seqs = []
    for entry in file_list:
        if len(entry) <= 2:
            continue
        nuc_seq = re.findall("[ATCG]+",entry)
        DNA_seqs.append(nuc_seq[0])
    return DNA_seqs


# Identifies the shortest DNA sequence in the list and from this sequence finds the common substrings shared between all the sequences.
def longestpat(file, length):
    DNA_seqs_sort = sorted(FASTA_to_list(file), key=len)
    shortest = DNA_seqs_sort[0]
    other = DNA_seqs_sort[1:]
    count = 0
    pattern = ""  #the substring
    shared_pattern = ""

    for i in range(len(shortest)):
        if len(shortest[i:i + length]) == length:
            pattern = shortest[i:i + length]
        # The below conditional statement ensures im not repeating the last pattern for the remaining i values in the loop that are shorter than the pattern
        if (len(shortest) - i) < len(pattern):
            break

        for j in range(len(other)):
            # Checks if that particular pattern is in all other sequences.
            if pattern in other[j]:
                count += 1
            if count == len(other):
                shared_pattern = pattern
                # If all the shared patterns need to be printed it should be done within this conditional statement.
        # Resets count for next pattern.
        count = 0

    # Recursively identifies all the common substrings among the sequences, incrementing the length by 1 each time.
    if isinstance(shared_pattern, str) and len(shared_pattern) > 1:
        print(shared_pattern,len(shared_pattern))
        return longestpat('Sample_data',length + 1)

    #The base condition that stops the recursive call is having a shared_pattern length above 1.
    else:
        return "we're done!"

print(longestpat('Sample_data',2))