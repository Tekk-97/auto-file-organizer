import os
import time

def create_dummy_files(folder, pattern="test", ext=".bin", count=5):
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        file_path = os.path.join(folder, f"{pattern}{i}{ext}")
        with open(file_path, "wb") as f:
            f.write(os.urandom(128))  # 128바이트짜리 더미 데이터
        print(f"생성됨: {file_path}")
        time.sleep(0.5)

if __name__ == "__main__":
    create_dummy_files("test_source", pattern="data", ext=".bin", count=5)
