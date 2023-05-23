import os, argparse
from PIL import Image

parser = argparse.ArgumentParser(description='Merge images into one')
parser.add_argument('-d', '--directory', type=str, help='Directory of images')
parser.add_argument('-o', '--output', type=str, help='Output file name')
args = parser.parse_args()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
if args.directory:
    im_dir = os.path.join(THIS_FOLDER, args.directory)
else:
    im_dir = THIS_FOLDER

max_height, max_width = 0, 0
files = sorted([i.lower() for i in os.listdir(im_dir) if i.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp'))])
for file in files:
    im_path = os.path.join(im_dir, file)
    with Image.open(im_path) as im:
        width, height = im.size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

image_count = len(files)
height = image_count // 2
if image_count % 2 == 1:
    height += 1

new_im = Image.new('RGBA', (2 * max_width, height * max_height), (0, 0, 0, 255))

cursor = 0
cursor2 = 0
for i, file in enumerate(files):
    im_path = os.path.join(im_dir, file)
    with Image.open(im_path) as im:
        if i % 2 == 0:
            new_im.paste(im, (cursor2 * max_width, cursor * max_height))
            cursor2 = 1
        else:
            new_im.paste(im, (i % 2 * max_width, cursor * max_height))
            cursor += 1
            cursor2 = 0

if image_count % 2 == 1:
    i += 1
    blank_image = Image.new('RGBA', (max_width, max_height), (43, 50, 61, 0))
    new_im.paste(blank_image, (i % 2 * max_width, cursor * max_height))

first_file = files[0]
if args.output:
    new_im.save(os.path.join(THIS_FOLDER, args.output))
else:
    new_im.save(os.path.join(THIS_FOLDER, 'merged.png'))
new_im.close()
