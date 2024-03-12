from PIL import Image

images = [Image.open(name) for name in ("stone.png",)]

colordb = set()

for im in images:
    width, height = im.size

    result = [i[:-1] for i in im.convert('RGBA').getdata()]
    colordb.update(set(result))

colordb = list(colordb)
f = open("output_file.txt", "w")
f.write(f"colordb = {colordb}")

for im in images:
    width, height = im.size
    name = im.filename[:im.filename.index(".")]

    result = [i[:-1] for i in im.convert('RGBA').getdata()]
    reflist = [colordb.index(i) for i in result]
    split_ref_list = [reflist[i*width:(i+1)*width] for i in range(height)]
    f.write(f"\n{name} = {split_ref_list}")
    
f.close()