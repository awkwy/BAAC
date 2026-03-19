input_file = "../data/data_raw/H_974_previous-2020-2024.csv"
output_file = "../data/data_raw/meteo_2024.csv"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    header = infile.readline()
    outfile.write(header)
    for line in infile:
        columns = line.strip().split(";")
        if columns[5].strip().startswith("2024"): 
            outfile.write(line)

print("Filtrage terminé.")