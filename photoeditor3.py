from PIL import Image, ImageDraw, ImageFont

img = Image.open("domo1.jpg")

draw = ImageDraw.Draw(img)

draw.rectangle((10,10,100,100), fill = (0, 255, 0), outline =(0,0,0))


#draw text on the image

font = ImageFont.truetype("arial.ttf", size = 20)
draw.text((100, 100), "Redtail", font = font, fill = (255, 0, 0))
img.save("edited_image.jpg")