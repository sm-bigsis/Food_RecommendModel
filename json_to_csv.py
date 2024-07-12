import os
import json
import csv

# JSON 파일이 저장된 폴더 경로 설정
json_folder_path = 'A:\바탕화면\C'  # JSON 파일이 저장된 폴더 경로로 변경하세요.
csv_file_path = 'food_type.csv'  # 저장할 CSV 파일 경로

# CSV 파일 생성 및 헤더 작성
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['code', 'name', 'fc', 'vg', 'cs', 'si', 'loc']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # JSON 파일들을 읽고 데이터 추출
    for json_filename in os.listdir(json_folder_path):
        if json_filename.endswith('.json'):
            with open(os.path.join(json_folder_path, json_filename), 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

                # 파일 이름에서 코드와 이름 추출
                file_name = data['data']['image_info']['file_name']
                code = file_name.split('_')[2]
                name = file_name.split('_')[3].split('.')[0]

                # food_type 데이터 추출
                food_type = data['data']['food_type']
                fc = food_type.get('fc', '')
                vg = food_type.get('vg', '')
                cs = food_type.get('cs', '')
                si = ', '.join(filter(None, food_type.get('si', [])))  # si 리스트를 문자열로 변환
                loc = food_type.get('loc', '')

                # CSV 파일에 데이터 작성
                writer.writerow({
                    'code': code,
                    'name': name,
                    'fc': fc,
                    'vg': vg,
                    'cs': cs,
                    'si': si,
                    'loc': loc
                })

print(f"CSV 파일이 '{csv_file_path}'에 저장되었습니다.")
