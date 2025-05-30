import os
import fnmatch
from tkinter import filedialog, simpledialog
from . import state
from .utils import natural_sort_key

def format_folder_display(folder, pattern, base_name):
    display_name = f"{folder} (패턴: {pattern}"
    if base_name:
        display_name += f", 기본 이름: {base_name}"
    display_name += ")"
    return display_name

def add_source_folder(ui_refs):
    listbox = ui_refs['source_listbox']
    output_box = ui_refs['output_box']
    update_folder_status = ui_refs['update_folder_status']

    if listbox.size() > 0:
        current_sel = listbox.curselection()
        if current_sel:
            default_path = state.source_folders[current_sel[0]]['folder']
        else:
            default_path = state.source_folders[-1]['folder']
        if not os.path.isdir(default_path):
            default_path = ""
        else:
            default_path = os.path.abspath(default_path)
    else:
        default_path = ""

    folder = filedialog.askdirectory(initialdir=default_path, mustexist=True)
    if not folder:
        return

    pattern = simpledialog.askstring("파일 패턴 입력", "이 폴더에서 추적할 파일 패턴을 입력하세요 (예: data*.png):")
    if pattern is None:
        output_box.insert('end', "파일 패턴 입력이 취소되었습니다.\n")
        output_box.see('end')
        return

    base_name = simpledialog.askstring("기본 이름 입력", "새 파일의 기본 이름을 입력하세요 (빈칸으로 두면 기본 이름을 사용하지 않습니다):")
    if base_name is None:
        output_box.insert('end', "기본 이름 입력이 취소되었습니다.\n")
        output_box.see('end')
        return

    state.source_folders.append({
        'folder': folder,
        'pattern': pattern,
        'base_name': base_name
    })
    display_name = format_folder_display(folder, pattern, base_name)
    listbox.insert('end', display_name)
    update_folder_status()
    output_box.insert('end', f"소스 폴더가 추가되었습니다: {display_name}\n")
    output_box.see('end')


def remove_source_folder(ui_refs):
    listbox = ui_refs['source_listbox']
    output_box = ui_refs['output_box']
    update_folder_status = ui_refs['update_folder_status']

    selected = listbox.curselection()
    if selected:
        index = selected[0]
        removed_folder = state.source_folders[index]
        listbox.delete(index)
        del state.source_folders[index]
        update_folder_status()
        output_box.insert('end', f"소스 폴더가 제거되었습니다: {removed_folder['folder']}\n")
        output_box.see('end')
    else:
        output_box.insert('end', "제거할 폴더를 선택하세요.\n")
        output_box.see('end')


def update_folder_status(ui_refs=None):
    listbox = None
    if ui_refs:
        listbox = ui_refs['source_listbox']
    for i, folder_info in enumerate(state.source_folders):
        folder = folder_info['folder']
        pattern = folder_info['pattern']
        try:
            file_list = os.listdir(folder)
        except Exception:
            continue
        matched_files = fnmatch.filter(file_list, pattern)
        files_present = len(matched_files) > 0
        status_color = "green" if files_present else "red"
        if listbox:
            listbox.itemconfig(i, {'bg': status_color})
