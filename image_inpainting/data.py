import tensorflow_io as tfio
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import Rescaling


drive_path = 'drive/MyDrive/Image_Inpainting/Data/imagenette2/train/'

# this function allows us to get the ds_train object for our dataset by taking
# the path to the dataset directory as a parameter
def get_ds(path=drive_path, img_height=256, img_width=256, batch_size=32):
    # loading data in batches from directory (to not overload ram)
    ds = tf.keras.preprocessing.image_dataset_from_directory(
        path,
        labels = 'inferred',
        label_mode = "int", # categorical, binary
        color_mode = "rgb", #loading jpg in rgb format
        batch_size = batch_size,
        image_size = (img_height,img_width), #reshape if not in this size, by default is 256*256
        shuffle = True, # to get a randomised order
        seed = 123)
        # validation_split = 0.1,
        # subset="training")
    return ds #this data is comprised of the images and the labels


# this function return the class names (i.e. labels) of the ds_train object
def get_class_names(ds):
    return ds.class_names


# function that converts ds_train images to lab and returns l channel and ab channel
def rgb_to_lab(image, label):
    lab_image = tfio.experimental.color.rgb_to_lab(image)
    return lab_image[:, :, :,0], lab_image[:, :, :,1:],lab_image, label
    # returns l channel, ab channels and labels
    # (TensorShape([32, 256, 256]), TensorShape([32, 256, 256, 2]), TensorShape([32]))


# the below function returns a series of batches of images in dataset format
# which have been converted to l and then also ab and b
def convert_to_lab(ds):
    #currently ds_train has rgb values from 0-255, the tensorflow fucntion that
    #converts rgb to lab accepts scaled rgb to 0-1 as input
    rescale = Rescaling(scale=1.0 / 255)
    rescaled_ds = ds.map(lambda image, label:(rescale(image), label))
    rescaled_ds_lab = rescaled_ds.map(rgb_to_lab)
    return rescaled_ds_lab  #this is an iterable object, contains three objects



# we have ds train which is a path to the dataset, allows to not load all at once
