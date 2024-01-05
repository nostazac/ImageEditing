from PIL import Image,ImageFilter

#load the uimage
img = Image.open("edited_image.jpg")

img = img.resize((1024, 720))

#flip the image
img = img.transpose(Image.FLIP_LEFT_RIGHT)

#apply gausiian blur horizontallly

img = img.filter (ImageFilter.GaussianBlur(radius=5))


#save the edited image

img.save("edited_image.jpg")