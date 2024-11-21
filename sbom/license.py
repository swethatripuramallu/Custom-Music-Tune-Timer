import re


def extract_licenses(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to match license IDs
    license_pattern = re.compile(r'"id":\s*"([^"]+)"')
    licenses = license_pattern.findall(content)

    # Use a set to filter out duplicates
    unique_licenses = set(licenses)

    return unique_licenses


def main():
    file_path = 'output.txt'
    licenses = extract_licenses(file_path)

    with open('licenses.txt', 'w') as file:
        for license_id in sorted(licenses):
            file.write(f"{license_id}\n")


if __name__ == "__main__":
    main()
