import os


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("Dir already created")


if __name__ == "__main__":
    create_dir("commercials")
    create_dir("television")
    create_dir("descriptors")
    create_dir("descriptors/commercials")
    create_dir("descriptors/television")
    create_dir("k_nearest")
