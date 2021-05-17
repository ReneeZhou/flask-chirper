import os
from PIL import Image
from secrets import token_hex
from flask import current_app


def save_image(form_image):
    # ramdonize user's image name so they don't collide in db
    random_hex = token_hex(8)
    # save the file with the same extension as user uploaded
    # if it's a file it will have this .filename attr from the form
    # throow away the first variable (f_name) because we won't need it 
    _, f_ext = os.path.splitext(form_image.filename)  
    picture_fn = random_hex + f_ext

    output_size = {'profile': (400, 400), 'background': (600, 200)}
    i = Image.open(form_image)

    if form_image.name == 'profile_image':
        picture_path = os.path.join(current_app.root_path, 'static/img/profile_pics', picture_fn)
        i.thumbnail(output_size['profile'])
    elif form_image.name == 'background_image':
        picture_path = os.path.join(current_app.root_path, 'static/img/background_pics', picture_fn)
        i.thumbnail(output_size['background'])
    
    i.save(picture_path)

    return picture_fn