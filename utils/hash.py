import hashlib


def hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


# print(hashlib.sha256("admin".encode()).hexdigest())
# print(hashlib.sha256("resident".encode()).hexdigest())
# admin
# 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918

# resident
# 84816ff383c826e9c11e26fdbd8d66e4edd7cf1ec1a4b23f8d10d84aa56e0d8f
