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
Autofile-organizer/
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

## 🔐 성능 및 안정성
``` 
- GUI는 tkinter의 after()를 이용하여 CPU 점유율 최소화
- 수동/자동 처리 선택 가능, 중복 실행 방지 및 상태 추적 포함
```
## 📄 라이선스

MIT License