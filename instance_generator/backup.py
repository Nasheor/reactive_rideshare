import shutil
import os
import time

def main():
    print("Saving instances")
    print(int(time.time()))
    src_dir = './instances'
    dst_dir = './history/1657797701'
    files = os.listdir(src_dir)
    shutil.copytree(src_dir, dst_dir)


if __name__=='__main__':
    main()