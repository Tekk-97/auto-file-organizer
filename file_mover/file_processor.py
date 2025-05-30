import os
import shutil
import fnmatch  # ✅ 이 줄 추가!
from tkinter import END
from . import state
from .utils import natural_sort_key


def finalize_file_move(source_file, new_name, ui_refs):
    new_file_path = os.path.normpath(os.path.abspath(os.path.join(state.target_folder, new_name)))

    try:
        shutil.move(source_file, new_file_path)
        ui_refs['output_box'].insert(
            END,
            f"파일 이동 완료: '{os.path.basename(source_file)}' -> '{new_file_path}'\n"
        )
    except Exception as e:
        ui_refs['output_box'].insert(
            END,
            f"파일 이동 실패: '{source_file}' -> '{new_name}' (오류: {e})\n"
        )
        ui_refs['processing_files'].discard(source_file)
        return

    ui_refs['processing_files'].discard(source_file)
    state.files_remaining_to_process -= 1
    if state.files_remaining_to_process == 0:
        state.processing_in_progress = False
        ui_refs['update_processing_status']()
        if ui_refs['auto_increment_count_var'].get():
            state.count += 1
            ui_refs['count_var'].set(str(state.count))
            ui_refs['save_settings'](ui_refs)
            ui_refs['output_box'].insert(END, f"카운트가 {state.count}로 증가했습니다.\n")
    ui_refs['output_box'].see(END)

def rename_and_move_file(source_file, new_name, ui_refs):
    ui_refs['output_box'].insert(
        END,
        f"파일 처리 중: '{os.path.basename(source_file)}' (대기: {state.wait_time // 1000}초)\n"
    )
    ui_refs['output_box'].see(END)
    ui_refs['root'].after(state.wait_time, lambda: finalize_file_move(source_file, new_name, ui_refs))

def process_files(ui_refs):
    if state.processing_in_progress:
        ui_refs['output_box'].insert(END, "작업 중입니다. 완료 후 시도하세요.\n")
        ui_refs['output_box'].see(END)
        return

    if not state.source_folders or not state.target_folder:
        ui_refs['output_box'].insert(END, "소스/타겟 폴더를 먼저 설정하세요.\n")
        ui_refs['output_box'].see(END)
        return

    files_to_process = []
    unmet_conditions = []

    for info in state.source_folders:
        folder = info['folder']
        pattern = info['pattern']
        base_name = info.get('base_name', '')

        if not os.path.isdir(folder):
            unmet_conditions.append(folder)
            continue

        try:
            files = sorted(fnmatch.filter(os.listdir(folder), pattern), key=natural_sort_key)
        except Exception as e:
            ui_refs['output_box'].insert(END, f"폴더 열기 실패: {folder} ({e})\n")
            ui_refs['output_box'].see(END)
            continue

        available = [
            os.path.abspath(os.path.join(folder, f))
            for f in files if os.path.isfile(os.path.join(folder, f)) and
            os.path.abspath(os.path.join(folder, f)) not in ui_refs['processing_files']
        ]

        if not available:
            unmet_conditions.append(folder)
            continue

        src_file = available[0]
        ext = os.path.splitext(src_file)[1]
        new_name = f"{base_name}{state.count}{ext}" if base_name else f"{state.count}{ext}"
        files_to_process.append((src_file, new_name))
        ui_refs['processing_files'].add(src_file)

    if unmet_conditions:
        ui_refs['output_box'].insert(
            END,
            f"조건 미충족 폴더 있음: {', '.join(unmet_conditions)}\n"
        )
        ui_refs['output_box'].see(END)
        return

    if not files_to_process:
        ui_refs['output_box'].insert(END, "처리할 파일이 없습니다.\n")
        ui_refs['output_box'].see(END)
        return

    state.processing_in_progress = True
    ui_refs['update_processing_status']()
    state.files_remaining_to_process = len(files_to_process)

    ui_refs['output_box'].insert(END, f"{len(files_to_process)}개 파일 처리 시작.\n")
    ui_refs['output_box'].see(END)

    for src, name in files_to_process:
        rename_and_move_file(src, name, ui_refs)

def update_processing_status(ui_refs):
    if state.processing_in_progress:
        ui_refs['status_label'].config(text="파일 처리 중...", fg="green")
    else:
        ui_refs['status_label'].config(text="대기 중", fg="blue")

def cancel_processing_action(ui_refs):
    state.cancel_processing = True
    ui_refs['output_box'].insert(END, "처리가 취소되었습니다. 현재 작업이 끝난 후 중단됩니다.\n")
    ui_refs['output_box'].see(END)
    update_processing_status(ui_refs)

def check_processing_conditions(ui_refs):
    if state.processing_in_progress:
        return
    # 간단하게 바로 처리 조건 체크 후 처리 시작
    process_files(ui_refs)
