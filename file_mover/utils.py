import re

def natural_sort_key(s):
    """
    숫자가 포함된 문자열을 자연스럽게 정렬하기 위한 키 반환 함수
    예: ["1.png", "10.png", "2.png"] -> 정렬 시 ["1.png", "2.png", "10.png"]
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]
