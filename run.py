import os
import subprocess

# Đường dẫn tới file jar và class chính
jar_path = "./executable_jar/kmeans_mapreduce.jar"
main_class = "Main"

# Các tham số chung cho lệnh Hadoop
base_input_dir = "./Resources/Input/Points/"  # Thư mục chứa các file points
base_state_dir = "./Resources/Input/Clusters/"  # Thư mục chứa các file clusters
base_input_dir_hadoop = "/KMeans/Resources/Input/Points/"
base_state_dir_hadoop = "/KMeans/Resources/Input/Clusters/"
output_dir = "/KMeans/Resources/Output"  # Thư mục đầu ra
number_of_reducers = "3"
delta = "100000000.0"
max_iterations = "30"
distance = "eucl"

# Tạo danh sách file points và clusters tương ứng
points_files = [f for f in os.listdir(base_input_dir) if f.startswith("points_")]
clusters_files = [f for f in os.listdir(base_state_dir) if f.startswith("clusters_")]

# Đảm bảo danh sách file points và clusters tương ứng
points_files.sort()
clusters_files.sort()
print(points_files)
print(clusters_files)
# Kiểm tra nếu số lượng file không khớp
if len(points_files) != len(clusters_files):
    print("Số lượng file points và clusters không khớp!")
    exit(1)

# Hàm chạy MapReduce cho một cặp file points và clusters
def run_mapreduce(points_file, clusters_file):
    input_file_path = os.path.join(base_input_dir_hadoop, points_file)
    state_path = os.path.join(base_state_dir_hadoop, clusters_file)
    current_output_dir = os.path.join(output_dir, os.path.splitext(points_file)[0])  # Đặt tên output theo file points

    # Xóa output cũ nếu tồn tại
    if os.path.exists(current_output_dir):
        subprocess.run(["hdfs", "dfs", "-rm", "-r", current_output_dir])

    # Cấu hình lệnh Hadoop
    command = [
        "hadoop", "jar", jar_path, main_class,
        "--input", input_file_path,
        "--state", state_path,
        "--number", number_of_reducers,
        "--output", current_output_dir,
        "--delta", delta,
        "--max", max_iterations,
        "--distance", distance
    ]

    # Chạy lệnh Hadoop
    print(f"Đang chạy MapReduce cho {points_file} và {clusters_file}...")
    subprocess.run(command, check=True)
    print(f"Hoàn thành xử lý {points_file}!")

# Lặp qua từng cặp file points và clusters để chạy MapReduce
for points_file, clusters_file in zip(points_files, clusters_files):
    run_mapreduce(points_file, clusters_file)

print("Hoàn tất xử lý tất cả các file.")


