
def is_file_format_valid(file, valid_extensions):
    return '.' in file and file.rsplit('.',1)[1].lower() in valid_extensions