from PIL import Image
import os

# 이미지 파일 이름을 리스트로 정의
img_path = 'crawling_results\\depth\\'


# 이미지 파일명을 저장할 리스트 초기화
image_files = []

# 폴더 내 모든 파일과 디렉토리 목록을 얻음
for filename in os.listdir(img_path):
    # 파일 확장자를 소문자로 변환하여 이미지 파일 필터링 (이미지 확장자에 따라 수정)
    if filename.lower().endswith(('.png')):
        image_files.append(filename)

# 이미지 파일의 절대 경로를 얻기 위해 경로 결합
image_paths = [os.path.join(img_path, image) for image in image_files]

batch_size = 6

# 이미지를 열고 조작
for i in range(0, len(image_files), batch_size):
    batch_images = []
    for j in range(i, min(i + batch_size, len(image_files))):
        image_path = os.path.join(img_path, image_files[j])
        image = Image.open(image_path)
        batch_images.append(image)

    # 이미지들을 가로 방향으로 이어붙일 경우
    result_image = Image.new('RGB', (sum(image.width for image in batch_images), batch_images[0].height))
    x_offset = 0
    for image in batch_images:
        result_image.paste(image, (x_offset, 0))
        x_offset += image.width

    # 결과 이미지를 저장할 경로
    output_folder = 'continuous_results'
    output_path = os.path.join(output_folder, 'output_'+str(i//6)+'.jpg')

    # 결과 이미지를 'continuous_results' 폴더에 저장
    os.makedirs(output_folder, exist_ok=True)  # 폴더 생성 (폴더가 이미 존재하면 오류가 발생하지 않음)
    result_image.save(output_path)
