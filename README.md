# K-Means MapReduce trong phân cụm ảnh
## Thành viên nhóm:
    1. Nguyễn Đức Anh - 22022661
    2. Vũ Việt Hùng - 22022585
    3. Hồ Minh Hoàng - 22022567
    4. Nguyễn Trọng Huy - 22022545
   
    5. Hà Kim Dương - 22022621
## [Link Báo cáo](https://github.com/anhduc1234567/bigdata_final_project/blob/main/slices_report_bigdata.pdf)
## [Link Slides](https://github.com/anhduc1234567/bigdata_final_project/blob/main/slices_report_bigdata.pdf)
## Chuẩn bị dữ liệu
`data_prep.py` chuẩn bị dữ liệu tạo file `clusters.txt` và `points.txt` cho từng ảnh.
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

## Installation

### Setup virtualenv
```bash
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```


### Chạy Kmeans MapReduce:
```
python run.py
```

### Chạy hiển thị hình ảnh cuối cùng:
```
python visualize_results.py --src_img ./sample_images --dst_folder_clusters ./Resources/Output --dst_img ./img_after_mapreduce

```
## Hình ảnh ban đầu
<div style="display: flex; justify-content: center; gap: 10px;">
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/sample_images/image4.png" alt="Hình minh họa" width="200"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/sample_images/image5.png" alt="Hình minh họa" width="300"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/sample_images/image3.jpg" alt="Hình minh họa" width="300"/>
</div>

## Hình ảnh trước khi chạy KMeans MapReduce
<div style="display: flex; justify-content: center; gap: 10px;">
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_no_mapreduce/tem_img1.png" alt="Hình minh họa" width="200"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_no_mapreduce/tem_img0.png" alt="Hình minh họa" width="300"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_no_mapreduce/tem_img3.png" alt="Hình minh họa" width="300"/>
</div>

## Sau khi KMeans MapReduce
<div style="display: flex; justify-content: center; gap: 10px;">
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_after_mapreduce/img_after1.png" alt="Hình minh họa" width="200"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_after_mapreduce/img_after0.png" alt="Hình minh họa" width="300"/>
<img src="https://github.com/anhduc1234567/bigdata_final_project/blob/main/img_after_mapreduce/img_after3.png" alt="Hình minh họa" width="300"/>
</div>
