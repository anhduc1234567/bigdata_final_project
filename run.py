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
max_iterations = "10"
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
def push_data(local_dir, hdfs_dir): # Kiểm tra và tạo thư mục trên HDFS nếu không tồn tại 
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_dir]) # Lặp qua từng file trong thư mục local 
    for file_name in os.listdir(local_dir): 
        local_file_path = os.path.join(local_dir, file_name) 
        hdfs_file_path = os.path.join(hdfs_dir, file_name) # Đẩy file từ local lên HDFS 
        #print(f"Đang đẩy file {local_file_path} lên {hdfs_file_path}...") 
        subprocess.run(["hdfs", "dfs", "-put", "-f", local_file_path, hdfs_file_path], check=True) 
        #print(f"Hoàn tất đẩy dữ liệu từ {local_dir} lên {hdfs_dir}.") # Đẩy dữ liệu points và clusters lên HDFS   
print('Dang put du lieu len hdfs')
push_data(base_input_dir, base_input_dir_hadoop) 
push_data(base_state_dir, base_state_dir_hadoop)
print('Complete !!')
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

    # Lấy đường dẫn thư mục output mới nhất
    last_dir_command = ["hadoop", "fs", "-ls", "-t", "-C", output_dir, "|", "head", "-1"]
    last_dir = subprocess.check_output(" ".join(last_dir_command), shell=True).decode().strip()
    
    # Hợp nhất và sắp xếp dữ liệu từ HDFS
    merged_output_path_hdfs = f"/KMeans/Resources/Output/{os.path.splitext(points_file)[0]}/clusters_{os.path.splitext(points_file)[0]}_out.txt"
    subprocess.run(
        f"hadoop fs -cat {last_dir}/1/part-r-[0-9][0-9][0-9][0-9][0-9] | "
        f"sort --numeric --key 1 | "
        f"hdfs dfs -put -f - {merged_output_path_hdfs}",
        shell=True,
        check=True
    )
    
    # Tải file output về local
    local_output_path = f"./Resources/Output/clusters_{os.path.splitext(points_file)[0]}_after.txt"
    subprocess.run(
        ["hdfs", "dfs", "-get", "-f", merged_output_path_hdfs, local_output_path],
        check=True
    )
    print(f"File output đã được tải về: {local_output_path}")


# Lặp qua từng cặp file points và clusters để chạy MapReduce
for points_file, clusters_file in zip(points_files, clusters_files):
    run_mapreduce(points_file, clusters_file)

print("Hoàn tất xử lý tất cả các file.")


