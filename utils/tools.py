def get_tables(file_path: str) -> set:
    with open(file_path, "r", encoding="UTF-8") as file:
        return set(file.readlines())
