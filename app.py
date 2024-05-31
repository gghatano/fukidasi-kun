import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

# 画像の読み込み
image_path = os.path.join(os.path.dirname(__file__), 'robot.png')
image = Image.open(image_path)

# Streamlit アプリの設定
st.title('吹き出しにテキストを入力')

# ユーザーからの入力を取得
user_text = st.text_area('ここにテキストを入力してください:', '')

# フォントサイズの選択
font_size = st.slider('フォントサイズを選択してください:', min_value=10, max_value=100, value=20)

# 日本語フォントの読み込み
font_path = os.path.join(os.path.dirname(__file__), 'NotoSansJP-Regular.otf')
font = ImageFont.truetype(font_path, font_size)

# テキストを画像に描画する関数
def draw_text(draw, text, position, font, max_width):
    # テキストを改行ごとに分割
    lines = []
    for line in text.split('\n'):
        # 各行のテキストを最大幅に合わせて分割
        words = line.split(' ')
        current_line = words[0]
        for word in words[1:]:
            if draw.textlength(current_line + ' ' + word, font=font) <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill='black')
        y += font.getsize(line)[1]

# テキストを画像に描画
if user_text:
    draw = ImageDraw.Draw(image)
    
    # 画像のサイズを取得
    image_width, image_height = image.size

    # テキストのバウンディングボックスを取得
    text_bbox = draw.textbbox((0, 0), user_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # テキストの配置場所を計算
    text_x = (image_width - text_width) // 2
    text_y = int(image_height * 0.25)

    # テキストを描画
    draw_text(draw, user_text, (text_x, text_y), font, image_width - 40)  # 40px padding

    # 画像を表示
    st.image(image, caption='吹き出しにテキストが追加された画像')

    # 画像を保存してダウンロードリンクを作成
    output_image_path = os.path.join(os.path.dirname(__file__), 'output.png')
    image.save(output_image_path)
    with open(output_image_path, 'rb') as file:
        btn = st.download_button(
            label="画像をダウンロード",
            data=file,
            file_name="output.png",
            mime="image/png"
        )

