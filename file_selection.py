import os
import re
import shutil

# 원본 파일이 저장된 루트 디렉토리 경로를 설정합니다.
source_root_directory = r'A:\바탕화면\음식 정보\TL\TL1\C'  # 원본 루트 디렉토리 경로로 변경하세요.

# 새 폴더 경로를 설정합니다.
destination_directory = r'A:\바탕화면\C'  # 새 폴더 경로로 변경하세요.

# 새 폴더가 존재하지 않으면 생성합니다.
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# C02001~C02149의 이름을 포함하고 .json으로 끝나는 파일 패턴 설정
pattern = re.compile(r'C_06_C060[0-1][0-9]_.*\.json')

# 코드 추적을 위한 집합 생성
codes_found = set()

# 파일 패턴에 맞는 파일 목록 찾기
file_list = []
for root, dirs, files in os.walk(source_root_directory):
    for file in files:
        match = pattern.match(file)
        if match:
            code = match.group(0)[5:11]  # 코드 추출
            if code not in codes_found:
                codes_found.add(code)
                file_list.append(os.path.join(root, file))
                print(f"파일을 찾았습니다: {os.path.join(root, file)}")  # 디버깅 메시지

# 파일을 새 폴더로 복사합니다.
for file in file_list:
    shutil.copy(file, destination_directory)
    print(f"파일이 {destination_directory} 폴더로 복사되었습니다: {file}")

if not file_list:
    print("조건에 맞는 파일을 찾지 못했습니다.")
else:
    print(f"총 {len(file_list)}개의 파일이 복사되었습니다.")







