import cv2
import math
import numpy as np
import os
import argparse
from pathlib import Path

from sklearn.neighbors import NearestNeighbors
from DescriptorAdministrator import CommercialDescriptors
from DescriptorAdministrator import TelevisionDescriptors


class CommercialDecider:

    def __init__(self, _video_dict):
        self.video_dict = _video_dict

    def get_frames_distance(self, actual_tuppla, next_tuppla):
        actual_tuppla_1 = (actual_tuppla[0])[0]
        actual_tuppla_2 = (actual_tuppla[0])[1]
        next_tuppla_1 = (next_tuppla[0])[0]
        next_tuppla_2 = (next_tuppla[0])[1]
        min_1 = min(abs(actual_tuppla_1 - next_tuppla_1), abs(actual_tuppla_1 - next_tuppla_2))
        min_2 = min(abs(actual_tuppla_2 - next_tuppla_1), abs(actual_tuppla_2 - next_tuppla_2))
        return abs(min(min_1, min_2))

    def get_commercials(self, video_name, list_of_targets, k):
        text = open("detecciones.txt", "w")
        list_of_tuples = np.load("k_nearest/" + video_name + ".npy")
        success_count = 0
        miss_count = 0
        same_frame_count = 0
        for i in range(len(list_of_tuples) - 1):
            actual_tuppla = list_of_tuples[i]
            next_tuppla = list_of_tuples[i + 1]
            actual_diff = (actual_tuppla[0])[1] - (actual_tuppla[0])[0]
            tupplas_diff = (next_tuppla[0])[0] - (actual_tuppla[0])[0]

            if (abs(tupplas_diff) < 10):
                if (success_count == 0):
                    first_time = actual_tuppla[1]
                success_count += 1
                miss_count = 0

                if (tupplas_diff == 0):
                    same_frame_count = same_frame_count + 1
                    if (same_frame_count == 10):
                        success_count = 0
                        same_frame_count = 0
                else:
                    same_frame_count = 0


            else:
                same_frame_count = 0
                if (success_count > 30):
                    init_time = first_time
                    duration = actual_tuppla[1] - first_time
                    commercial_name = self.video_dict[list_of_targets[(actual_tuppla[0])[0]]]
                    string_to_write = video_name + "\t" + str(round(init_time, 1)) + "\t" + str(
                        round(duration, 1)) + "\t" + commercial_name
                    print(string_to_write)
                    text.write(string_to_write + "\n")
                success_count = 0
        text.close()


def convert_to_matrix(list_of_commercial_descriptors):
    concat_array = np.array([])
    i = 0
    for list_of_descriptors in list_of_commercial_descriptors:
        if i == 0:
            concat_array = list_of_descriptors
            i = 1
        else:
            concat_array = np.concatenate((concat_array, list_of_descriptors), axis=0)
    return concat_array


def save_k_nearest(program_name, descriptors, neigh, k=3):
    list_k_nearest = []
    i = 0
    for descriptor in descriptors:
        k_nearest = neigh.kneighbors(np.array([descriptor]), k, return_distance=False)
        k_nearest = np.squeeze(k_nearest)
        seconds = i / 3.0
        tuppla = (k_nearest, seconds)
        list_k_nearest.append(tuppla)
        i = i + 1

    np.save('k_nearest/' + program_name + '.npy', list_k_nearest)


'''Via rapida para crear los descriptores.
'''


def create_all_commercial_descriptors(descriptors_path='descriptors/commercials/', commercial_path='commercials/'):
    commercial_manager = CommercialDescriptors(descriptors_path, commercial_path)
    commercial_manager.create_all_descriptors()


def create_all_television_descriptors(_descriptor_path='descriptors/television/', _videos_path='television/'):
    television_manager = TelevisionDescriptors(_descriptor_path, _videos_path)
    television_manager.create_all_descriptors()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', '--source', dest='video_source', default='example.jpg',
                        help='Give me the path of your video')
    args = parser.parse_args()

    a = CommercialDescriptors()
    b = TelevisionDescriptors()

    '''Load descriptores
    '''
    list_of_descriptors, list_of_targets = a.load_all_descriptors()
    list_of_targets = convert_to_matrix(list_of_targets)
    list_of_descriptors = convert_to_matrix(list_of_descriptors)
    video_dict, class_dict = a.get_dict()

    '''Creates a file for de k nearest neighbors of each frame
    '''
    video_name = b.get_video_name(args.video_source)
    descriptor = b.load_descriptors(video_name)
    neigh = NearestNeighbors(3)
    neigh.fit(list_of_descriptors)
    save_k_nearest(video_name, descriptor, neigh)

    '''Creates the file "Detecciones.txt"
    '''
    d = CommercialDecider(video_dict)
    d.get_commercials(video_name, list_of_targets, 3)





