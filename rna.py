import os
import re

def generate_chunks(sequence, N, M):
    chunks = [sequence[i:i+N] for i in range(0, len(sequence), M)]
    return chunks

def save_to_file(chunks, output_directory, rna_seq_name):
    os.makedirs(output_directory, exist_ok = True)
    file_name = os.path.join(output_directory, f"{rna_seq_name}.txt")
    with open(file_name, 'w') as file:
        for i, chunk in enumerate(chunks, start=1):
            file.write(chunk + "\n\n")
    print(f"Saved chunks for {rna_seq_name} to {file_name}") 

if __name__ == "__main__":
    with open("sequence.fasta", "r") as fasta_file:
        fasta_lines = fasta_file.readlines()

    sequences = []
    current_sequence = ""
    current_name = ""
    for line in fasta_lines:
        if line.startswith(">"):
            if current_sequence:
                sequences.append((current_name, current_sequence))
                current_sequence = ""
            current_name = line.strip()[1:12]  
        else:
            current_sequence += line.strip()

    if current_sequence:
        sequences.append((current_name, current_sequence))

    N = 10
    M = 1
    output_directory = "split_sequences"

    for name, sequence in sequences:
        sequence = sequence.replace('\n', '')
        chunks = generate_chunks(sequence, N, M)
        save_to_file(chunks, output_directory, name)  
