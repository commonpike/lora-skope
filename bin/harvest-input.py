import re, os
from PIL import Image
from pathlib import Path
from random import randint
import sys

#input_folders = [
#    "folder1",
#    "folder2"
#]

input_folders = sys.argv[1:]



dirname = os.path.dirname(__file__)
output_folder = os.path.join(dirname, '../input')
os.makedirs(output_folder, exist_ok=True)

TARGET_SIZE = 512

pattern = re.compile(r'\.(jpe?g|png)$', re.IGNORECASE)



for input_folder in input_folders:
    print("Processing " + input_folder + "...")
    for path in Path(input_folder).rglob('*'):
        if pattern.search(path.name):
    

            input_path = os.path.join(input_folder, path)
            input_filename = os.path.basename(path)
            rndid = randint(10000000,99999999)
            output_filename = str(rndid) + "-" +input_filename
            output_path = os.path.join(output_folder, output_filename)
            print(input_path)
            #print(output_filename)
            #continue

            img = Image.open(input_path).convert("RGB")

            if img.width >= TARGET_SIZE or img.height >= TARGET_SIZE:
                # Resize keeping aspect ratio
                img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)

                # Create new square image and paste centered
                new_img = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), (0, 0, 0))
                x_offset = (TARGET_SIZE - img.width) // 2
                y_offset = (TARGET_SIZE - img.height) // 2
                new_img.paste(img, (x_offset, y_offset))

                print("Writing "+output_path+"...")
                new_img.save(output_path)
            else:
                # If already square and small enough, just copy
                print("Skipping small "+input_path+"...")
