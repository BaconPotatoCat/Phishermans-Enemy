import os

try:
    print("Installing dependancies...")
    os.system("pip3 install -r requirements.txt")
    print("Done.")
except Exception as e:
    print("Error occured while installing dependancies:",e)
    sys.exit(-1)