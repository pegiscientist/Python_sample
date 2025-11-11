#Write program to read Blast results. Extract Query, BestHit, Evalue, and Identities.

import os
import re

#Print the current directory
current_directory = os.getcwd()
print(f"Current Directory: {current_directory}")

#List files in the current directory
files_in_directory = os.listdir(current_directory)
if files_in_directory:
    print("Files in the current directory:")
    for file in files_in_directory:
        print(f"- {file}")
else:
    print("No files in the current directory.")

#Prompt user to enter file path
file_path = input("Enter the filename or path to the BLAST results: ").strip()

#Check if the file exists, if not, print message and quit
if not os.path.isfile(file_path):
    print("The specified file does not exist")
    exit()

#Function to parse BLAST results
def parse_blast_results(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    results = []
    best_hit = []
    best_hit_lines = []
    query = ""
    evalue = ""
    identities = ""
    in_hit_section = False

    for line in lines:
        line = line.strip()

        #Extract Query
        if line.startswith("Query="):
            best_hit_lines = []
            query = line.split("Query=")[1].strip()
            evalue = ""
            identities = ""
            in_hit_section = False

        #Start of Best Hit section
        elif line.startswith(">") and not best_hit_lines:
            in_hit_section = True
            #best_hit_lines.append(line[1:].strip()) # Remove '>'
            best_hit_lines.append(line.strip())

        #Extract Best Hit data
        elif in_hit_section:

            #Extract E-value
            match = re.search(r"Expect\s*=\s*([^\s,]+)", line)
            if match:
                evalue = match.group(1)
       
            #Extract the best hit lines
            match = re.search(r"\b(?:Score|Length|Identities|Frame)\b", line)
            if match is None:
                best_hit_lines.append(line.strip())

        #Extract Identities and finish record
        if line.startswith("Identities =") and not identities:
            identities = line.split(",")[0].split("=")[1].strip()
            
            #Retrieved all info to assemble a record
            #Join multiple lines of Best Hit
            best_hit = ' '.join(best_hit_lines)
            results.append((query, best_hit, evalue, identities))

    return results         

#Parse the BLAST results
parse_results = parse_blast_results(file_path)

#Write results to output file
output_file = "BlastOutput.txt"
with open(output_file, 'w') as out_file:
    # Define column widths
    query_width = 15
    besthit_width = 30
    evalue_width = 15
    identities_width = 15

    # Write header
    header = f"{'Query':<{query_width}} {'BestHit':<{besthit_width}} {'E-value':<{evalue_width}} {'Identities':<{identities_width}}\n"
    out_file.write(header)
    out_file.write("-" * (query_width + besthit_width + evalue_width + identities_width + 3) + "\n")

    for record in parse_results:
        query, best_hit, evalue, identities = record
        query = query[:query_width]
        evalue = evalue[:evalue_width]
        identities = identities[:identities_width]

        # Split BestHit into 30-character chunks
        besthit_chunks = [best_hit[i:i+besthit_width] for i in range(0, len(best_hit), besthit_width)]

        # First line includes Query, first chunk of BestHit
        out_file.write(f"{query:<{query_width}} {besthit_chunks[0]:<{besthit_width}} {evalue:<{evalue_width}} {identities:<{identities_width}}\n")
        # Remaining chunks only under BestHit
        for chunk in besthit_chunks[1:]:
            out_file.write(f"{'':<{query_width}} {chunk:<{besthit_width}} {'':<{evalue_width}} {'':<{identities_width}}\n")
    

print(f"BLAST results have been written to {output_file} ({len(parse_results)} entries).")

