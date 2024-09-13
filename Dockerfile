FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄下的所有檔案
COPY . /app

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定啟動時運行的命令
CMD ["python", "app.py"]