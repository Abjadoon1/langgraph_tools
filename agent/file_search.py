from pathlib import Path


def find_file(filename):
    project_folder = Path(__file__).resolve().parent.parent
    matches = list(project_folder.rglob(filename))

    if not matches:
        return {"status": "not_found", "matches": []}

    elif len(matches) == 1:
        return {"status": "found", "matches": [str(matches[0])]}

    return {"status": "multiple_matches", "matches": [str(path) for path in matches]}


def search_file(file_path, query):
    matches = []

    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            match_index = line.lower().find(query.lower())
            if match_index == -1:
                continue

            start = max(0, match_index - 100)
            end = match_index + len(query) + 100
            snippet = line[start:end].strip()
            result = {"line": line_number, "snippet": snippet.strip()}
            matches.append(result)

    if matches:
        return matches
    return "query not found in given file"
