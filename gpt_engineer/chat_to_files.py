import re

def parse_file_name(file_name):
    pattern = r"[^\w\s.]"
    name = re.sub(pattern, '', file_name)
    return name.strip()


def parse_chat(chat):  # -> List[Tuple[str, str]]:
    # Get all ``` blocks and preceding filenames
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        # Strip the filename of any non-allowed characters and convert / to \
        path = re.sub(r'[<>"|?*]', "", match.group(1))

        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        # Get the code
        code = match.group(2)

        # Add the file to the list
        files.append((path, code))

    # Get all the text before the first ``` blockj
    readme = chat.split("```")[0]
    files.append(("README.md", readme))

    print(files)

    # Return the files
    return files

def store_output(filename,chat, workspace):
    workspace[filename] = chat

def to_files(chat, workspace):
    store_output("all_output.txt", chat, workspace)

    files = parse_chat(chat)
    
    for file_name, file_content in files:
        name = parse_file_name(file_name)
        workspace[name] = file_content
