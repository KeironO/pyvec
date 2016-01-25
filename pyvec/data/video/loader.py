import cv2, numpy as np, random, csv, os
from scipy import misc

def load_labels_and_file_name(tsv_file, directory):
    tsv_list = []
    with open(tsv_file, "rb") as tsv:
        reader = csv.reader(tsv, delimiter="\t", lineterminator="\n")
        for files in reader:
            if os.path.isfile(directory+"/"+files[0]) == True:
                tsv_list.append(files)
            else:
                print "Not found!"
        return tsv_list

def random_array(video_frames, desired_number_of_frames):
    list = []
    list.extend(range(0, video_frames))
    random_list = []
    for x in range(desired_number_of_frames):
        random_list.append(random.choice(list))
    return random_list

def load_video_vector(directory, tsv_file, height, width):
    labels_file_name = load_labels_and_file_name(tsv_file, directory)
    number_of_videos = len(labels_file_name)
    data = np.empty((number_of_videos, n_frames, height, width), dtype="float32")
    data.flatten()
    labels = np.empty((number_of_videos, ), dtype=np.dtype("a16"))
    for i, details in enumerate(labels_file_name):
        video = cv2.VideoCapture(directory+details[0])
        for x in range(n_frames):
            return_value, frame = video.read()
            if return_value == False:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = misc.imresize(frame, (height, width))
            data[i:x:,:,:] = frame
            labels[i] = details[1]
    return data, labels

