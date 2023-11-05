def open_read(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)