import cv2
import numpy as np
import os
from pathlib import Path


class DescriptorAdministrator:
    """This class is a super class template like for creation and administration of descriptors

       Attributes:
              descriptors_path (str): Is the path for the descriptors.
              videos_path (str): Is the path where the videos are save.
              list_of_descriptors (list): A list that contains the list of descriptors of the current video.
              rate_of_extracting (int): The rate of extraction on the videos, in this case we assume a default value of 10, therefore, 
              one on ten of the frames. This is done under the assumption that the video are on 30 FPS.
              resize (int): We use resizing to create the descriptors. The default value in this case is 10x10 pixels.
    """

    def __init__(self, _descriptors_path, _videos_path, _rate_of_extracting=10, _resize=10):
        self.descriptors_path = _descriptors_path
        self.videos_path = _videos_path
        self.list_of_descriptors = []
        self.rate_of_extracting = _rate_of_extracting
        self.resize = _resize

    def save_descriptors(self, video_name):
        """Saves the descriptors on the self's descriptors path.

           Args:
                   video_name (str): Video name used for the creation of the descriptor.

           Returns:
                   Nothing
        """
        pass

    def load_descriptors(self, video_name):
        """Load the descriptors files for one video.

           Args:
                   video_name (str): Video name used for the creation of the descriptor.

           Returns:
                   Nothing
        """
        pass

    def create_descriptors(self, video_name, video_format):
        """Creates a descriptor by shrinking the image to a size of a pixels
           and then flatting the image to create a vector.

           Args:
                   video_name (str): Video name used for the creation of the descriptor.
                video_format (str): Video format of the actual video.

           Returns:
                Nothing

        """
        video = cv2.VideoCapture(self.videos_path + video_name + video_format)
        success = video.grab()
        count = 0
        while success:
            if count == 0 or (count % self.rate_of_extracting == 0):
                success, image = video.retrieve()
                flat_descriptor = self.create_flat_descriptor(image)
                self.append_descriptor(flat_descriptor, video_name)
            success = video.grab()
            count += 1
        self.save_descriptors(video_name)

    def create_flat_descriptor(self, image):
        """Creates a flat descriptor from an image
           First shrink the image and then flats it.

           Args:
                    image (numpy.ndarray): image used for creating the descriptor.

           Returns: 
                   (numpy.ndarray) A flat descriptor of a image.
        """

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray_image, (self.resize, self.resize))
        flat_descriptor = resized_image.reshape(1, self.resize ** 2)
        return np.squeeze(flat_descriptor)

    def append_descriptor(self, flat_descriptor, video_name):
        """Appends the actual frame descriptor to the list of descriptors of the current video.

           Args:
                   flat_descriptor (numpy.ndarray): Is a flat descriptor of an image.
                   video_name (str): Video name used for the creation of the descriptor.

           Returns:
                   Nothing
        """
        self.list_of_descriptors.append(flat_descriptor)

    def get_video_name(self, video_name):
        """Gets a video name from the file's name.

           Args:
                   video_name (str): video name with the extension.

           Returns:
                   (str): the video name without the extension.
        """

        return video_name[:video_name.index(".")]

    def create_all_descriptors(self):
        """Creates and saves all the descriptors of the videos on the self videos_path.
        """
        list_of_videos = os.listdir(self.videos_path)
        for video in list_of_videos:
            if self.is_created(self.get_video_name(video)):
                print("already created")
                continue

            self.create_descriptors(self.get_video_name(video))

    def load_all_descriptors(self):
        """Loads all the descriptors on the self descriptors path.
        """
        pass

    def is_created(self, video_name):
        """Verify if the descriptor is created.
        """
        pass

    def clean(self):
        """Clean the descriptors variables of the class.
        """
        self.list_of_descriptors = []


class CommercialDescriptors(DescriptorAdministrator):
    """Commercial descriptor class that inherits from descriptor administrator

       Attributes: 
              target (list): list of the class number.
              video_dict (dictionary)
    """

    def __init__(self, _descriptor_path='descriptors/commercials/', _videos_path='commercials/'):
        super().__init__(_descriptor_path, _videos_path)
        self.target = []
        self.video_dict = {}
        self.class_dict = {}
        self.create_dict()

    def create_dict(self):
        videos = os.listdir(self.videos_path)
        i = 0
        for video_file in videos:
            video_name = video_file[:video_file.index(".")]
            self.video_dict[i] = video_name
            self.class_dict[video_name] = i
            i += 1

    def get_dict(self):
        return self.video_dict, self.class_dict

    def save_descriptors(self, commercial_name):
        if self.is_created(commercial_name):
            print("File already created")
            return
        np.save(self.descriptors_path + commercial_name + '_descriptors' + '.npy', self.list_of_descriptors)
        np.save(self.descriptors_path + commercial_name + '_target' + '.npy', self.target)
        self.clean()

    def load_descriptors(self, commercial_name):
        if self.is_created(commercial_name):
            descriptors = np.load(self.descriptors_path + commercial_name + '_descriptors' + '.npy')
            targets = np.load(self.descriptors_path + commercial_name + '_target' + '.npy')
            return descriptors, targets
        print("Files not found")
        return False

    def append_descriptor(self, flat_descriptor, commercial_name):
        super().append_descriptor(flat_descriptor, commercial_name)
        self.target.append(self.class_dict[commercial_name])

    def create_descriptors(self, tv_name, video_format='.mpg'):
        super().create_descriptors(tv_name, video_format)

    def load_all_descriptors(self):
        list_of_videos = os.listdir(self.videos_path)
        list_of_descriptors = []
        list_of_targets = []
        for video in list_of_videos:
            descriptors, targets = self.load_descriptors(self.get_video_name(video))
            list_of_descriptors.append(descriptors)
            list_of_targets.append(targets)
        return list_of_descriptors, list_of_targets

    def is_created(self, commercial_name):
        descriptor = Path(self.descriptors_path + commercial_name + '_descriptors' + '.npy')
        target = Path(self.descriptors_path + commercial_name + '_target' + '.npy')
        return descriptor.exists() and target.exists()

    def clean(self):
        super().clean()
        self.target = []


class TelevisionDescriptors(DescriptorAdministrator):

    def __init__(self, _descriptor_path='descriptors/television/', _videos_path='television/'):
        super().__init__(_descriptor_path, _videos_path)

    def save_descriptors(self, tv_name):
        if self.is_created(tv_name):
            print("File already created")
            return
        np.save(self.descriptors_path + tv_name + '_descriptors' + '.npy', self.list_of_descriptors)
        super().clean()

    def load_descriptors(self, tv_name):
        if self.is_created(tv_name):
            return np.load(self.descriptors_path + tv_name + '_descriptors' + '.npy')
        print("File not found")
        return False

    def create_descriptors(self, tv_name, video_format='.mp4'):
        print(tv_name)
        super().create_descriptors(tv_name, video_format)

    def load_all_descriptors(self):
        list_of_videos = os.listdir(self.videos_path)
        list_of_descriptors = []
        for video in list_of_videos:
            descriptors = self.load_descriptors(self.get_video_name(video))
            list_of_descriptors.append(descriptors)
        return list_of_descriptors

    def is_created(self, tv_name):
        descriptor = Path(self.descriptors_path + tv_name + '_descriptors' + '.npy')
        return descriptor.exists()

