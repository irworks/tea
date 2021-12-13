import hashlib


def calculate_hash(file_name):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as file:
        while True:
            data = file.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return format(sha1.hexdigest())

