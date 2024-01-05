import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image , ImageTk , ImageFilter,ExifTags, ImageOps, ImageEnhance, ImageDraw, ImageFont
import cv2
import numpy as np
# from mrcnn import visualize
# from mrcnn.config import Config
# from mrcnn.model import MaskRCNN
# from mrcnn import model


# class CustomConfig(Config):
#     NAME = "custom"
#     images_per_GPU = 1
#     NUM_CLASSES = 1 + 80
    
# def remove_background():
#     global current_image
    
#     if current_image:
#         image = np.array(current_image)
#         results = model.detect([image], verbose = 0)
#         r = results[0]
#         #create a mask for the detected object
#         mask = r['masks'][:, :, 0]
        
#         #apply the mask to the image
#         result = image.copy()
#         result[mask] = [0, 0, 0]
        
#         current_image - Image.fromarray(result)
#         display_image(current_image)
        
#     # Load the pretrained model masj R-CNN model
    
#     mosel = MaskRCNN(mode = "interface", model_dir = "./", config = CustomConfig())
#     model.load_weights("mask_rcnn_coco.h5", by_name = True)
        
        
        
        
zoom_factor = 1.0
current_image = None
original_image = None
undo_history = []
redo_history = []
text_items = []
contrast_var = tk.DoubleVar
brightness_var = tk.DoubleVar
color_var = tk.DoubleVar
is_dark_theme = False
#variables to text entry
text_to_add = ""
adding_text = False
 
# Func to open image
def open_image():
    
    global file_path, original_image, current_image, zoom_factor
    file_path = filedialog.askopenfilename()
    
    if file_path:
    
        original_image = Image.open(file_path)
        current_image = original_image.copy()
        display_image(current_image)
        
def display_image(img):
    
    global zoom_factor, img_tk
    
    img.thumbnail((1366 * zoom_factor, 768 * zoom_factor)) # resize photo
    img_tk = ImageTk.PhotoImage(img)
    image_label.img = img_tk
    image_label.config(image = img_tk)
    image_label.image = img_tk
    
    
# func to apply grayscale
def apply_grayscale():
    global current_image
    if current_image:
        undo_history.append(current_image.copy())
        current_image = ImageOps.grayscale(current_image)
        display_image(current_image)
        redo_history.clear()
    
# Crop effects

def apply_crop():
    global current_image
    if current_image:
        current_image = ImageOps(current_image)
        current_image = current_image.crop((200, 2000, 250, 250)) # Replace with your coordinates
        display_image(current_image)

def apply_oil_painting():
    
    global current_image
    if  current_image:
        undo_history.append(current_image.copy())
        current_image = current_image.filter(ImageFilter.EMBOSS)
        display_image(current_image)
        redo_history.clear()
    
def zoom_in(img):
    
    global zoom_factor,current_image
    zoom_factor *= 1.2
    img.thumbnail((int(700 * zoom_factor), int (700 * zoom_factor)))
    display_image(current_image)
    
def zoom_out(img):
    
    global zoom_factor,current_image
    zoom_factor /= 1.2
    img.thumbnail((int(700 * zoom_factor), int (700 * zoom_factor)))
    display_image(current_image)
    
def compare_images():
    if original_image:
        display_image(original_image)
def save_image():
    if current_image:
        save_path = filedialog.asksaveasfilename(defaultextension= ".png")
        
        if save_path:
            current_image.save(save_path)
            
def undo():
    global current_image
    
    if undo_history:
        redo_history.append(current_image. copy()) 
        current_image = undo_history.pop()  
        display_image(current_image)

def redo():
    global current_image
    if redo_history:
        undo_history.append(current_image.copy())
        current_image = redo_history.pop()
        display_image(current_image)
        
def add_text():
    global adding_text
    adding_text = True
    text_entry.pack()

#function to place text on the image
def place_text(event):
    
    global current_image, text_to_add,text_items,adding_text
    adding_text = True
    
    if current_image and adding_text:
        text = text_to_add
        
        if text:
            undo_history.append(current_image.copy())
            new_image = current_image.copy()
            draw = ImageDraw.Draw(new_image)
            font = ImageFont.truetype("arial.ttf", 30)
            text_items.append(new_image)
            draw.text((event.x, event.y), text, fill= "red", font = font)
            display_image(new_image)
            redo_history.clear()
        text_entry.delete(0, tk.END)
        text_entry.pack_forget()
        adding_text = False

def remove_background():
    global current_image
    
    if current_image:
        cv2_image = cv2.cvtColor(np.array(current_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(cv2_image)
        cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
        result = cv2.bitwise_and(cv2_image, mask)
        current_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        display_image(current_image)
        
def apply_filters(filter_name):
        global current_image
         
        if current_image:
            if filter_name == "Blur":
                current_image = current_image.filter(ImageFilter.BLUR)
            elif filter_name == "Contour":
                current_image = current_image.filter(ImageFilter.CONTOUR)
            elif filter_name == "Detail":
                current_image = current_image.filter(ImageFilter.DETAIL)
            elif filter_name == "Edge Enhance":
                current_image = current_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_name == "Emboss":
                current_image = current_image.filter(ImageFilter.EMBOSS)
            elif filter_name == "Sharpen":
                current_image = current_image.filter(ImageFilter.SHARPEN)
            elif filter_name == "Smooth":
                current_image = current_image.filter(ImageFilter.SMOOTH_MORE)
            elif filter_name == "Enhance Brightness":
                enhancer = ImageEnhance.Brightness(current_image)
                current_image = enhancer.enhance(1.5)
            elif filter_name == "Enhance Contrast":
                enhancer = ImageEnhance.Contrast(current_image)
                current_image = enhancer.enhance(1.5)
            elif filter_name == "Enhance Color":
                enhancer = ImageEnhance.Color(current_image)
                current_image = enhancer.enhance(1.5)
            
            
            
            display_image(current_image)

           
#Adjust brightness
def adjust_brightness(value):
    
    value = brightness_scale.get()   
    global current_image,original_image
    
    if original_image:
        
        if value == 0.0:
            
            #reset the brightness to original value
            current_image = current_image.copy()
            
        else:
            
            current_image = original_image.copy()
            enhancer = ImageEnhance.Brightness(current_image)
            current_image = enhancer.enhance(value)
            
        display_image(current_image)

def adjust_contrast(value):
    
    value = contrast_scale.get()
    global current_image,original_image
    
    if original_image:
        
        if value == 0.0:
            #reset the original image
            current_image = current_image.copy()
            
        else:
            current_image = original_image.copy()
            enhancer = ImageEnhance.Contrast(current_image)
            current_image = enhancer.enhance(value)      
        display_image(current_image)
        
def adjust_color(value):
    
    value = color_scale.get()
    
    global current_image, original_image
    
    if original_image:
        
        if  value == 0.0:
            
            #reset the color value to original value
            current_image = current_image.copy()
            
        else:
            
            current_image = original_image.copy()
            enhancer = ImageEnhance.Color(current_image)
            current_image = enhancer.enhance(value)
        display_image(current_image)
        
        
        
        
def change_theme():
    global is_dark_theme
    
    if is_dark_theme:
        
        root.configure(bg = "white")
        frame.configure(bg = "lightgray")
        is_dark_theme = False
        
    else:
        
        root.configure(bg = "black")
        frame.configure(bg = "gray")
        is_dark_theme = True
        
# def display_img_properties():
#     global original_image
    
#     properties_text = "Image Properties: \nWidth: {}\nHeight: {}\nFromat: {}"
#     properties_text = properties_text.format(original_image.width, original_image.height,original_image.format)
    
#     #window to diaplay the properties
#     properties_window = tk.Toplevel(root)
#     properties_window.title("Image Properties")
    
#     properties_label = tk.Label(properties_window, text = properties_text)
#     properties_label.pack(padx=20, pady = 20)
    
def display_image_properties():
    
    global img_tk,original_image
    if 'img_tk' not in globals():
        return
    
    properties_text = "Image Properties:\n"
    properties_text += f"Width: {img_tk.width}:\n"
    properties_text += f"Height: {img_tk.height}:\n"
    properties_text += f"Format: {original_image.format}:\n"
    
    #extract and display omage metadata
    metadata = original_image.info
    if metadata:
        properties_text += "\nMetadata:\n"
        for key, value in metadata.items():
            properties_text += f"{key}: {value} \n"\
                
    #extract and display EXIF data
    exif_data = get_exif_data()
    if exif_data:
        properties_text += "\nEXIF Data: \n"
        
        for tag, value in exif_data.items():
            properties_text += f"{tag}: {value} \n"
            
    #window to display 
    properties_window = tk.Toplevel(root)
    properties_window.title("Image Properties")
    
    properties_label = tk.Label(properties_window, text= properties_text, justify = "left")
    properties_label.pack(padx = 20, pady = 20)
    
def get_exif_data():
    
    global original_image
    
    exif_data = {}
    
    try:
        for tag, value in original_image.getexif().items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            exif_data[tag_name] = value
    except AttributeError:
        pass
    
    return exif_data
    
    
root = tk.Tk()
root.title('Image Editor')

frame = tk.Frame(root, bg = "black")
frame.grid(row=0, column=0, sticky = "nswe")

#create a menu bar
menu_bar = tk.Menu(root, bg = "gray", font=("Arial", 12))
root.config(menu = menu_bar)

# Create a File menu with dropdown options
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label = "File", menu= file_menu)
file_menu.add_command(label="Open Image", command = open_image)
file_menu.add_separator()
file_menu.add_command(label="Image Properties", command = display_image_properties)
file_menu.add_command(label="Exit", command = root.quit())


#add the edit menu
edit_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Edit", menu = edit_menu)

# Create a Filter menu with dropdown options
filter_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label="Filter", menu = filter_menu)

#Add filter menu options to the dropdown menu
filter_options = ["Blur", "Contour", "Detail", "Edge Enhance", "Emboss", "Sharpen", "Smooth","Enhace Brightness", "Enhance Contrart", "Enhance Color"]
for filter_name in filter_options:
    filter_menu.add_command(label = filter_name, command = lambda f = filter_name: apply_filters(f))

# Create the wwindow menu
window_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Window",menu = window_menu)
# window_menu.add_command(label = "Fullscreen", command = root.attributes('-fullscreen', not root.attributes('-fullscreen')))
window_menu.add_command(label = "Change theme", command = change_theme)
#window_menu.add_command(label= "Change Image Frame Style", command=image_frame_style)


#create the language menu
language_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Language", menu = language_menu)

#Create the help menu
help_menu = tk.Menu(menu_bar, tearoff = 0)
menu_bar.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "for help please visit https://www.4toeditor/help/operation/")

draw_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label = "Draw", menu= draw_menu)

grayscale_button = tk.Button(frame, text = "Grayscale", command=apply_grayscale, bg = "red", fg = "white", padx = 10,  pady=5, relief = tk.RAISED, borderwidth=5)
crop_button = tk.Button(frame, text = "Crop", command = apply_crop, bg = "green", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
oil_painting_buttom = tk.Button(frame, text = "Oil Painting", command = apply_oil_painting, bg = "red", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
zoom_in_button = tk.Button(frame, text = "Zoom In", command = zoom_in, bg = "green", fg = "white", padx = 10 ,pady=5, relief = tk.RAISED, borderwidth=5)
zoom_out_button = tk.Button(frame, text = "Zoom Out", command = zoom_out, bg = "purple", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
compare_button = tk.Button(frame, text = "Compare", command = compare_images, bg = "orange", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
save_button = tk.Button(frame, text = "Save", command = save_image, bg = "Black", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
undo_button = tk.Button(frame, text = "Undo", command = undo, bg = "green", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
redo_button = tk.Button(frame, text = "Redo", command = redo, bg = "red", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
add_text_button = tk.Button(frame, text = "Add Text", command = add_text, bg = "green", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)
bg_remove_button = tk.Button(frame, text = "remove background", command = remove_background, bg = "Yellow", fg = "white", padx = 10, pady=5, relief = tk.RAISED, borderwidth=5)


grayscale_button.grid(row = 0, column=0, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
crop_button.grid(row=1, column=0, padx = 10, columnspan = 2, pady = 10, sticky = "ew")
oil_painting_buttom.grid(row=2,column=0, columnspan = 2, padx= 10, pady = 10, sticky = "ew")
zoom_in_button.grid(row=3,column=0, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
zoom_out_button.grid(row = 4, columnspan = 2 ,column = 0, padx = 10, pady = 10, sticky = "ew")
compare_button.grid(row=5, column =0, columnspan = 2, padx = 10, pady = 10, sticky = "ew")
save_button.grid(row=6, column=0, padx = 10, pady = 10, sticky = "ew")
undo_button.grid(row=7, column=0, padx = 10, pady = 10, sticky = "ew")
redo_button.grid(row=8, column=0, padx = 10, pady = 10, sticky = "ew")
add_text_button.grid(row=9, column=0, padx = 10, pady = 10, sticky = "ew")
bg_remove_button.grid(row=10, column=0, padx = 10, pady = 10, sticky = "ew")



# Create an entry for adding text
text_entry = tk.Entry(frame)
text_entry.pack_forget() # Hide the entry field

# Create a frame for the imagr section eoth ehite bacjground
image_frame = tk.Frame(root, bg = "white")
image_frame.grid(row = 0, column = 1, rowspan = 1, columnspan = 1,sticky="nswe")


#label to display the image
image_label = tk.Label(image_frame, text = "Image Display Area", bg = "White")
image_label.pack(expand = True, fill = "both")

# Brightness, contrast and color frame
adjust_frame = tk.Frame(root, bg = "black")
adjust_frame.grid(row = 2, column = 0, columnspan=1, sticky="nsew")

# Creating slider for adjust brightness
#brightness_scale = ttk.Scale(frame, from_ = 0.1, to = 2.0, variable = brightness_var, orient = "horizontal",command= lambda v = brightness_var:adjust_brightness(v))

brightness_scale  = tk.Scale(adjust_frame, from_ = 0.1, to = 2.0, variable = brightness_var, orient="horizontal",command = adjust_brightness)
brightness_label = tk.Label(adjust_frame, text = "Brightness")
brightness_label.grid(row = 0, column = 2, rowspan= 2, sticky="ew")
brightness_scale.grid(row = 0, column = 3, rowspan= 2, sticky="ew") 
brightness_var = tk.DoubleVar()
brightness_var.set(1.0)
#brightness_scale.bind("<Motion>", lambda event, s = brightness_scale: adjust_brightness(s.get()))

# Creating slider for adjust contrast
#contrast_scale = ttk.Scale(frame ,from_ = 0.1, to = 2.0, variable = contrast_var, orient = "horizontal" ,command= lambda v = contrast_var:adjust_contrast(v) )
contrast_scale  = tk.Scale(adjust_frame, from_ = 0.1, to = 2.0, variable = contrast_var, orient="horizontal",command = adjust_contrast)
contrast_label = tk.Label(adjust_frame,text = "Contrast")
contrast_label.grid(row = 0, column=5)
contrast_scale.grid(row=0, column=6)
contrast_var = tk.DoubleVar()
contrast_var.set(1.0)
#contrast_scale.bind("<Motion>", lambda event, s = contrast_scale: adjust_contrast(s.get()))

# Creating slider for adjust color
#color_scale = ttk.Scale(frame, from_ = 0.1, to = 2.0, variable = color_var, orient = "horizontal" ,command= lambda v = contrast_var:adjust_contrast(v) )
color_scale  = tk.Scale(adjust_frame, from_ = 0.1, to = 2.0, variable = color_var, orient="horizontal",command = adjust_color)
color_label = tk.Label(adjust_frame, text = "Color")
color_label.grid(row=0, column=8)
color_scale.grid(row=0, column = 9)
color_var = tk.DoubleVar()
color_var.set(1.0)
#color_scale.bind("<Motion>", lambda event, s = color_scale: adjust_color(s.get()))

#initialize the file path variable
file_path = None

#bind mouse click event for placing text
image_label.bind("<Button-1>", place_text)


root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.mainloop()
    