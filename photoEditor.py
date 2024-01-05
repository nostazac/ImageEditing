from PIL import Image, ImageEnhance, ImageFilter
import os

path = './domo1'
pathout = "/.image path"

for filename in os.listdir(path):
    img = Image.open(f"{path} / {filename}")
    
    edit = img.filter(ImageFilter.SHARPEN).convert('L').rotate(-90)
    
    factor = 1.5
    
    enhancer = ImageEnhance.Contrast(edit)
    
    clean_name = os.path.splitext(filename)[0]
    
    edit.save(f'.{pathout} / {clean_name}_edited.jpg')