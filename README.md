# K-Means Mapreduce trong phân cụm ảnh
## Chuẩn bị dữ liệu
`data_prep.py` chuẩn bị dữ liệu tạo file  `clusters.txt` và `points.txt` cho từng ảnh.
```
python data_prep.py --src_img ./sample_images --dst_folder_points ./Resources/Input/Points --dst_folder_clusters ./Resources/Input/Clusters --dst_img ./img_no_mapreduce --k_init_centroids 10
```
### Các tham số:
    - src_img : nguồn dẫn tới tập ảnh.
    - dst_folder_points: nơi lưu trữ các points đầu ra.
    - dst_folder_clusters: nơi lưu trũ các clusters đầu ra.
    - dst_img: nơi lưu trữ ảnh đầu ra (ảnh sau khi phân cụm ngẫu nhiên)
### Requirements
- Python 3 (tested on version 3.8.2)
- numpy (tested on version 1.19.2)
- opencv (tested on version 4.4.0.42)
- Chạy môi trường Hadoop

### Installation

## Setup virtualenv
```bash
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```
.

## Chạy Kmeans-Mapreduce:
```
python run.py
```

## Chạy hiển thị hình ảnh cuối cùng:
```
python visualize_results.py --src_img ./sample_images --dst_folder_clusters ./Resources/Output --dst_img ./img_after_mapreduce

```
