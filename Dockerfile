# ベースイメージ
FROM python:3.9

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# フォントの配置
RUN curl -O http://fonts.gstatic.com/ea/notosansjapanese/v6/download.zip
RUN unzip ./download.zip -d ./

# アプリケーションのコピー
COPY . .

# Streamlitを起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

