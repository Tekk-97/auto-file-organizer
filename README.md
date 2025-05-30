# 파일 이동 자동화 도구 📂

지정한 폴더에서 특정 패턴의 파일을 감지하고, 지연 시간 후 이름을 바꾸어 타겟 폴더로 이동합니다.GUI를 통해 카운트 조절, 자동 처리, 대기 시간 설정 등 다양한 옵션을 제공합니다.

## 🔧 주요 기능
```
- 다중 소스 폴더 지정
- 파일 패턴 기반 자동 감지 (예: data*.png)
- 파일 이동 시 이름 자동 변경 (count, 기본 이름)
- GUI 기반 조작 (Tkinter 기능 포함)
- 자동 처리 (소스 폴더 조건 확인 및 처리 자동 시작)
- 처리 중 진행 상태 표시 (상황 레이블, 목록 창 및 출력창)
- 설정 자동 저장/로드 (settings.json)
- 취소 버튼으로 처리 중단 가능
- 카운트를 수동으로 조절 가능 (UI에서 버튼 제공)
```
## 실행 방법
```
bash
python -m file_mover
```
file_mover 폴더는 반드시 __init__.py가 있어야 하며, 그 상위 폴더에서 실행해야 합니다.

## 📁 폴더 구조 예시
``` 
auto-file-organizer/
├── file_mover/            # 주요 소스 디렉토리
│   ├── __main__.py       # 실행 진입점
│   ├── gui.py            # GUI 구성 및 이벤트 바인딩
│   ├── file_processor.py # 파일 이동 및 이름 변경 처리
│   ├── settings.py       # 설정 저장/불러오기 관리
│   ├── folder_manager.py # 소스/타겟 폴더 관리 기능
│   ├── state.py          # 전역 상태 변수 관리
│   └── utils.py          # 자연 정렬 등 유틸 함수
├── README.md
├── requirements.txt
├── .gitignore
└── settings.json
```

## 🧪 테스트 도구
```
- dummy_file_generator.py: 테스트용 더미 파일 자동 생성기
- run.bat: 윈도우에서 더블클릭으로 실행 가능한 배치 파일
```
## 🧠 코드 설명 (모듈별 함수 포함)
```
gui.py
- start_gui(): GUI 창을 초기화하고 위젯을 배치, 각 이벤트 핸들러와 모듈 함수 연결.
- choose_target_folder(): 타겟 폴더 선택 다이얼로그 띄움.
- update_count(change, ui_refs): 카운트 값을 수동으로 증가/감소.
- update_wait_time(ui_refs): 대기 시간(seconds)을 입력받아 내부 상태로 반영.


file_processor.py
- process_files(ui_refs): 소스 폴더 목록을 순회하여 조건을 만족하는 파일을 수집하고 처리.
- rename_and_move_file(source_file, new_name, ui_refs): 일정 시간 후 파일 이동 예약.
- finalize_file_move(source_file, new_name, ui_refs): 실제로 파일을 이동하고 진행 상태 및 카운트를 갱신.
- update_processing_status(ui_refs): 현재 처리 상태를 라벨에 표시.
- cancel_processing_action(ui_refs): 처리 작업 중 취소 요청 처리.
- check_processing_conditions(ui_refs): 처리 전 조건 확인 후 process_files 호출.

settings.py
- load_settings(ui_refs): settings.json을 읽어 GUI 상태에 반영.
- save_settings(ui_refs): 현재 GUI 상태와 설정을 JSON 파일로 저장.
- reset_settings(ui_refs): GUI 및 내부 상태를 초기화하고 저장 파일 갱신.

folder_manager.py
- format_folder_display(folder, pattern, base_name): 리스트에 표시할 폴더 설명 문자열 구성.
- add_source_folder(ui_refs): 폴더 선택 및 패턴/기본이름 입력 후 리스트에 추가.
- remove_source_folder(ui_refs): 선택된 소스 폴더를 리스트와 내부 목록에서 제거.
- update_folder_status(ui_refs): 각 소스 폴더 내 조건 만족 여부를 리스트에 색으로 반영.

state.py
- count: 파일 이름 숫자 증가용 기준값
- wait_time: 파일 이동 전 대기 시간 (ms)
- source_folders: 소스 폴더 목록 [{folder, pattern, base_name}]
- target_folder: 이동 대상 폴더
- cancel_processing: 취소 요청 플래그
- processing_in_progress: 현재 처리 중 여부
- processing_files: 중복 방지용 현재 처리 중 파일 집합
- files_remaining_to_process: 현재 처리할 파일 수
- last_folder_status: 자동 처리 비교용 마지막 상태 캐시

utils.py
- natural_sort_key(s): 문자열 내 숫자를 기준으로 자연 정렬하는 key 함수
```

## 🔐 성능 및 안정성
``` 
- GUI는 tkinter의 after()를 이용하여 CPU 점유율 최소화
- 수동/자동 처리 선택 가능, 중복 실행 방지 및 상태 추적 포함
```
## 📄 라이선스

MIT License
