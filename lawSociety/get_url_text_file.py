import json

jsonl_file_path = "sra_solicitors.jsonl"

# Open and iterate through the JSONL file

all_urls = []


with open(jsonl_file_path, "r", encoding="utf-8") as file:
    for line in file:
        try:
            data = json.loads(line.strip())  # Parse JSON line
            sra_number = data.get("sra_number")  # Get SRA number if available
            url = f"https://solicitors.lawsociety.org.uk/search/results?Pro=True&Type=1&Name={sra_number}"
            if sra_number:
                all_urls.append(sra_number)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


with open("all_sra_numbers.txt", "w", encoding="utf-8") as output_file:
    for url in all_urls:
        output_file.write(url + "\n")