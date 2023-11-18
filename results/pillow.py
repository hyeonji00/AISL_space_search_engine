from PIL import Image
import os

# 이미지 파일 이름을 리스트로 정의
img_path = 'crawling_results\\depth\\'
image_files = ['-1.09,-17.65,5,0.png', '-1.09,-17.65,5,1.png', '-1.09,-17.65,5,2.png', '-1.09,-17.65,5,3.png', '-1.09,-17.65,5,4.png', '-1.09,-17.65,5,5.png']

# 이미지 파일의 절대 경로를 얻기 위해 경로 결합
image_paths = [os.path.join(img_path, image) for image in image_files]

# 이미지를 열고 조작
images = [Image.open(image) for image in image_paths]


# 이미지들을 가로 방향으로 이어붙일 경우
result_image = Image.new('RGB', (sum(image.width for image in images), images[0].height))
x_offset = 0
for image in images:
    result_image.paste(image, (x_offset, 0))
    x_offset += image.width

# 결과 이미지를 저장할 경로
output_folder = 'stitching_results'
output_path = os.path.join(output_folder, 'output.jpg')

# 결과 이미지를 'stitching_results' 폴더에 저장
os.makedirs(output_folder, exist_ok=True)  # 폴더 생성 (폴더가 이미 존재하면 오류가 발생하지 않음)
result_image.save(output_path)
