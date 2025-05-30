import json
import os
from .state import (
    PROGRAM_VERSION, SETTINGS_FILE,
    source_folders, target_folder, count, wait_time,
)
from . import state
from .utils import natural_sort_key

def load_settings(ui_refs):
    """
    UI 요소를 넘겨 받아서 설정값을 GUI에 반영함
    ui_refs: {
        'count_var', 'wait_time_var', 'target_folder_var',
        'auto_increment_count_var', 'source_listbox', 'output_box',
        'update_folder_status'
    }
    """
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)

        if settings.get('version') != PROGRAM_VERSION:
            raise ValueError("설정 파일 버전 불일치")

        state.count = settings.get('count', 1)
        state.wait_time = settings.get('wait_time', 1000)
        state.target_folder = settings.get('target_folder', '')

        ui_refs['count_var'].set(str(state.count))
        ui_refs['wait_time_var'].set(str(state.wait_time // 1000))
        ui_refs['target_folder_var'].set(state.target_folder)
        ui_refs['auto_increment_count_var'].set(settings.get('auto_increment_count', True))

        state.source_folders.clear()
        ui_refs['source_listbox'].delete(0, 'end')

        for folder_info in settings.get('source_folders', []):
            folder = folder_info.get('folder')
            pattern = folder_info.get('pattern')
            base_name = folder_info.get('base_name', '')
            state.source_folders.append({
                'folder': folder,
                'pattern': pattern,
                'base_name': base_name
            })

            display_name = f"{folder} (패턴: {pattern}"
            if base_name:
                display_name += f", 기본 이름: {base_name}"
            display_name += ")"
            ui_refs['source_listbox'].insert('end', display_name)

        ui_refs['update_folder_status']()
        ui_refs['output_box'].insert('end', "설정 파일이 정상적으로 로드되었습니다.\n")
        ui_refs['output_box'].see('end')

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        ui_refs['output_box'].insert('end', f"설정 파일을 초기화합니다. (오류: {e})\n")
        ui_refs['output_box'].see('end')
        reset_settings(ui_refs)
        save_settings(ui_refs)


def save_settings(ui_refs):
    settings = {
        'version': PROGRAM_VERSION,
        'count': state.count,
        'wait_time': state.wait_time,
        'target_folder': state.target_folder,
        'auto_increment_count': ui_refs['auto_increment_count_var'].get(),
        'source_folders': [
            {
                'folder': info['folder'],
                'pattern': info['pattern'],
                'base_name': info.get('base_name', '')
            }
            for info in state.source_folders
        ]
    }

    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def reset_settings(ui_refs):
    state.count = 1
    state.wait_time = 1000
    state.target_folder = ''
    state.source_folders.clear()

    ui_refs['count_var'].set(str(state.count))
    ui_refs['wait_time_var'].set(str(state.wait_time // 1000))
    ui_refs['target_folder_var'].set(state.target_folder)
    ui_refs['auto_increment_count_var'].set(True)

    ui_refs['source_listbox'].delete(0, 'end')
    ui_refs['update_folder_status']()
    ui_refs['output_box'].insert('end', "설정 파일이 초기화되었습니다.\n")
    ui_refs['output_box'].see('end')
