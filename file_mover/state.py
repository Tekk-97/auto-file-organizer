# 프로그램 버전
PROGRAM_VERSION = "25.03.12"

# 설정 관련
SETTINGS_FILE = 'settings.json'

# 전역 상태 변수들
count = 1
wait_time = 1000  # milliseconds
source_folders = []  # [{'folder': ..., 'pattern': ..., 'base_name': ...}]
target_folder = ""
cancel_processing = False
processing_in_progress = False
processing_files = set()
files_remaining_to_process = 0
last_folder_status = {}  # 폴더 상태 캐시
