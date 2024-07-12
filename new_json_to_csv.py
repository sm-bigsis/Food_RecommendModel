import os
import json
import pandas as pd

def get_category(code):
    # 대분류 결정
    if code.startswith('A'):
        large_category = '특수외식메뉴'
    elif code.startswith('B'):
        large_category = '일반외식 및 배달음식'
    elif code.startswith('C'):
        large_category = '끼니 대체 메뉴'
    elif code.startswith('D'):
        large_category = '음료 및 차류'
    else:
        large_category = 'Unknown'

    # 중분류 결정
    sub_code = code[1:3]
    if sub_code == '01':
        medium_category = '떡'
    elif sub_code == '02':
        medium_category = '빵'
    elif sub_code == '03':
        medium_category = '죽'
    elif sub_code == '04':
        medium_category = '수프'
    elif sub_code == '05':
        medium_category = '샌드위치'
    elif sub_code == '06':
        medium_category = '기타'
    elif sub_code == '07':
        medium_category = '과일 및 과채음료'
    elif sub_code == '08':
        medium_category = '유제품'
    elif sub_code == '09':
        medium_category = '잎차류'
    elif sub_code == '10':
        medium_category = '커피류'
    elif sub_code == '11':
        medium_category = '배달음식'
    elif sub_code == '12':
        medium_category = '일반외식'
    elif sub_code == '13':
        medium_category = '향토음식'
    elif sub_code == '14':
        medium_category = '외국음식'
    else:
        medium_category = 'Unknown'

    return large_category, medium_category


def json_to_csv(json_folder_path, output_csv_path):
    data = []

    # JSON 폴더 내 모든 파일 순회
    for json_file in os.listdir(json_folder_path):
        if json_file.endswith('.json'):
            file_path = os.path.join(json_folder_path, json_file)

            # JSON 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                
                # 파일명에서 6자리 코드와 음식 이름 추출 
                file_name = os.path.splitext(json_file)[0]
                parts = file_name.split('_')
                code = parts[2]
                food_name = parts[3]

                # 대분류와 중분류 추출
                large_category, medium_category = get_category(code)

                # food_type 데이터 추출
                food_type = content['data']['food_type']

                # 'si' 리스트를 문자열로 변환하되, None 값을 제거
                si_list = food_type.get('si', [])
                si_list = [str(item) for item in si_list if item is not None]
                si_str = ', '.join(si_list)

                # 데이터 추가
                data.append({
                    'Code': code,
                    'Food Name': food_name,
                    '대분류': large_category,
                    '중분류': medium_category,
                    'fc': food_type.get('fc'),
                    'vg': food_type.get('vg'),
                    'cs': food_type.get('cs'),
                    'si': si_str
                })

    # 데이터프레임으로 변환
    df = pd.DataFrame(data)
    
    # CSV 파일로 저장
    df.to_csv(output_csv_path, index=False, encoding='utf-8')

# JSON 파일이 저장된 폴더 경로
json_folder_path = 'C:\\Users\\지수\\Desktop\\JSON files'
# 출력 CSV 파일 경로
output_csv_path = 'output.csv'

# 함수 호출
json_to_csv(json_folder_path, output_csv_path)
