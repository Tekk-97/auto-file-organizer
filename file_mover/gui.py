import tkinter as tk
from tkinter import END
from . import state
from .settings import load_settings, save_settings, reset_settings
from .folder_manager import add_source_folder, remove_source_folder, update_folder_status
from .file_processor import (
    process_files, check_processing_conditions,
    cancel_processing_action, update_processing_status
)

def start_gui():
    root = tk.Tk()
    root.title(f"파일 이동 도구 - by LCM {state.PROGRAM_VERSION}")

    # 바인딩할 변수
    count_var = tk.StringVar(value=str(state.count))
    wait_time_var = tk.StringVar(value=str(state.wait_time // 1000))
    target_folder_var = tk.StringVar()
    auto_increment_count_var = tk.BooleanVar(value=True)
    auto_process = tk.BooleanVar()

    # UI 요소 모음
    ui_refs = {
        'root': root,
        'count_var': count_var,
        'wait_time_var': wait_time_var,
        'target_folder_var': target_folder_var,
        'auto_increment_count_var': auto_increment_count_var,
        'processing_files': state.processing_files,
        'status_label': None,  # 아래에서 채움
        'output_box': None,    # 아래에서 채움
        'source_listbox': None,  # 아래에서 채움
        'update_processing_status': lambda: update_processing_status(ui_refs),
        'save_settings': lambda refs: save_settings(refs),
        'update_folder_status': lambda: update_folder_status(ui_refs),
    }

    # GUI 구성
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 소스 폴더
    tk.Label(main_frame, text="소스 폴더:").grid(row=0, column=0, padx=2, sticky="e")
    source_listbox = tk.Listbox(main_frame, height=5, width=50)
    source_listbox.grid(row=0, column=1, padx=2, sticky="we")
    ui_refs['source_listbox'] = source_listbox

    source_list_scrollbar_x = tk.Scrollbar(main_frame, orient="horizontal", command=source_listbox.xview)
    source_list_scrollbar_x.grid(row=1, column=1, padx=2, sticky="ew")
    source_listbox.config(xscrollcommand=source_list_scrollbar_x.set)

    folder_buttons_frame = tk.Frame(main_frame)
    folder_buttons_frame.grid(row=0, column=2, rowspan=2, padx=2)
    tk.Button(folder_buttons_frame, text="+ 폴더 추가", width=10,
              command=lambda: add_source_folder(ui_refs)).pack(fill=tk.X)
    tk.Button(folder_buttons_frame, text="- 폴더 제거", width=10,
              command=lambda: remove_source_folder(ui_refs)).pack(fill=tk.X)

    # 타겟 폴더
    tk.Label(main_frame, text="타겟 폴더:").grid(row=2, column=0, padx=2, sticky="e")
    target_entry = tk.Entry(main_frame, textvariable=target_folder_var, width=40)
    target_entry.grid(row=2, column=1, padx=2, sticky="we")
    tk.Button(main_frame, text="선택", width=10, command=lambda: choose_target_folder(target_folder_var, ui_refs)).grid(row=2, column=2)

    # 카운트
    tk.Label(main_frame, text="카운트 값:").grid(row=3, column=0, padx=2, sticky="e")
    count_entry = tk.Entry(main_frame, textvariable=count_var, width=10)
    count_entry.grid(row=3, column=1, sticky="w")
    tk.Button(main_frame, text="카운트 변경", width=10,
              command=lambda: update_count(0, ui_refs)).grid(row=3, column=1, sticky="e")

    count_buttons = tk.Frame(main_frame)
    count_buttons.grid(row=3, column=2)
    tk.Button(count_buttons, text="▲", width=2, command=lambda: update_count(1, ui_refs)).grid(row=0, column=0)
    tk.Button(count_buttons, text="▲5", width=3, command=lambda: update_count(5, ui_refs)).grid(row=0, column=1)
    tk.Button(count_buttons, text="▼", width=2, command=lambda: update_count(-1, ui_refs)).grid(row=1, column=0)
    tk.Button(count_buttons, text="▼5", width=3, command=lambda: update_count(-5, ui_refs)).grid(row=1, column=1)

    # 대기 시간
    tk.Label(main_frame, text="대기 시간(초):").grid(row=4, column=0, padx=2, sticky="e")
    wait_entry = tk.Entry(main_frame, textvariable=wait_time_var, width=10)
    wait_entry.grid(row=4, column=1, sticky="w")
    tk.Button(main_frame, text="대기 시간 변경", width=10,
              command=lambda: update_wait_time(ui_refs)).grid(row=4, column=1, sticky="e")

    # 파일 처리 버튼들
    tk.Button(main_frame, text="파일 처리", width=10,
              command=lambda: check_processing_conditions(ui_refs)).grid(row=5, column=0, pady=5)
    tk.Button(main_frame, text="취소", width=10,
              command=lambda: cancel_processing_action(ui_refs)).grid(row=5, column=1, sticky="w")

    # 자동 처리 체크박스
    tk.Checkbutton(main_frame, text="자동 파일 처리 (1초마다)", variable=auto_process).grid(row=6, column=0, columnspan=2, sticky="w")
    tk.Checkbutton(main_frame, text="파일 처리 후 카운트 +1", variable=auto_increment_count_var).grid(row=7, column=0, columnspan=2, sticky="w")

    # 상태 라벨
    status_label = tk.Label(main_frame, text="대기 중", fg="blue", width=20, anchor="w")
    status_label.grid(row=8, column=0, columnspan=3, sticky="w")
    ui_refs['status_label'] = status_label

    # 출력창
    output_box = tk.Text(root, height=10, width=70)
    output_box.pack(fill=tk.BOTH, expand=True)
    ui_refs['output_box'] = output_box

    # 초기 설정 불러오기
    load_settings(ui_refs)
    update_folder_status(ui_refs)

    def on_closing():
        save_settings(ui_refs)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


# 추가 보조 함수들
def choose_target_folder(target_folder_var, ui_refs):
    from tkinter import filedialog
    folder = filedialog.askdirectory()
    if folder:
        state.target_folder = folder
        target_folder_var.set(folder)
        ui_refs['output_box'].insert(END, f"타겟 폴더가 설정되었습니다: {folder}\n")
        ui_refs['output_box'].see(END)

def update_count(change, ui_refs):
    try:
        state.count = int(ui_refs['count_var'].get()) + change
        ui_refs['count_var'].set(str(state.count))
        ui_refs['output_box'].insert(END, f"카운트가 {state.count}로 변경되었습니다.\n")
        ui_refs['output_box'].see(END)
    except ValueError:
        ui_refs['output_box'].insert(END, "유효하지 않은 카운트 값입니다.\n")
        ui_refs['output_box'].see(END)

def update_wait_time(ui_refs):
    try:
        state.wait_time = int(ui_refs['wait_time_var'].get()) * 1000
        ui_refs['output_box'].insert(END, f"대기 시간이 {state.wait_time // 1000}초로 변경되었습니다.\n")
        ui_refs['output_box'].see(END)
    except ValueError:
        ui_refs['output_box'].insert(END, "유효하지 않은 대기 시간입니다.\n")
        ui_refs['output_box'].see(END)
