import argparse
from os.path import join
from pathlib import Path
import cv2
import numpy as np
from os import listdir
from os.path import join, isdir, isfile
from os.path import isfile, join
from pathlib import Path

parser = argparse.ArgumentParser(description='This script creates points.txt and clusters.txt files for a given image.')

parser.add_argument('--src_img', type=str, help='Path to the source image.')

parser.add_argument('--dst_folder_clusters', type=str, help='Directory in which points.txt and clusters.txt will be saved.')
parser.add_argument('--dst_img', type=str, help='Path to the image to be written.')


args = parser.parse_args()

def load_nparray(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(np.array([float(num) for num in line.split(' ')]))

    return np.stack(data).astype(np.float64)
def nparray_to_str(X):
    to_save = '\n'.join([' '.join(str(X[i])[1:-1].split()) for i in range(len(X))])
    return to_save


# def main(src_img, dst_folder, k):
#     # files to be created
#     points_path = join(dst_folder, 'points.txt')
#     clusters_path = join(dst_folder, 'clusters.txt')

#     # create directory
#     Path(dst_folder).mkdir(parents=True, exist_ok=True)

#     # load and write points
#     img = cv2.imread(src_img).reshape((-1, 3)).astype(np.float32)
#     with open(points_path, 'w') as f:
#         f.write(nparray_to_str(img))
#     print(f'Points saved in: {points_path}')

#     # generate and save uniformly sampled centroids
#     s = np.random.uniform(low=img.min(), high=img.max(), size=(k, 3))
#     tmp_labels = np.arange(1, k + 1).reshape((k, 1))
#     clusters = np.hstack((tmp_labels, s))

#     with open(clusters_path, 'w') as f:
#         f.write(nparray_to_str(clusters))
#     print(f'Centroids saved in: {clusters_path}')
def nparray_to_str(arr):
    return '\n'.join(' '.join(map(str, row)) for row in arr)


def load_clusters(path):
    if isdir(path):
        files = glob(join(path, 'part-r-*[0-9]'))
    elif isfile(path):
        files = [path]
    else:
        raise Exception('Invalid file path.')

    centroids = [load_nparray(file)[:, 1:] for file in files]
    centroids = np.concatenate(centroids, axis=0).reshape(-1, centroids[0].shape[-1])
    return centroids
    
def cover_img(clusters_path, src_img, dst_img):
    clusters = load_clusters(clusters_path)
    img = cv2.imread(src_img)
    shape = img.shape

    img = img.reshape((-1, 3))
    new_image = np.zeros_like(img)
    for i in range(img.shape[0]):
        ind = np.linalg.norm(clusters - img[i], axis=-1).argmin()
        new_image[i] = clusters[ind].astype(np.uint8)

    cv2.imwrite(dst_img, new_image.reshape(shape))



def main(src_folder,dst_folder_clusters,dst_img):
    # create directory
    # Path(dst_folder).mkdir(parents=True, exist_ok=True)

    # list all image files in the folder
    img_files = [f for f in listdir(src_folder) if isfile(join(src_folder, f)) and f.endswith(('jpg', 'png', 'jpeg'))]

    for i in range(len(img_files)):
        src_img_path = join(src_folder, img_files[i])
        img_name = Path(img_files[i]).stem

        # files to be created for this image
        clusters_path = join(dst_folder_clusters, f'clusters_points_{i}_after.txt')
    
        # load and write points
        img = cv2.imread(src_img_path).reshape((-1, 3)).astype(np.float32)
        img_new_path = join(dst_img, f'img_after{i}.png')
        cover_img(clusters_path,src_img_path,img_new_path)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.src_img,args.dst_folder_clusters,args.dst_img)


