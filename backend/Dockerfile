FROM python:3.11-slim

WORKDIR /app

# 安装基础系统依赖
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright (先装python包)
RUN pip install playwright

# 安装 Chromium 浏览器
RUN playwright install chromium

# 安装浏览器依赖 (关键步骤) - 使用 playwright install-deps 自动安装所有依赖
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libdbus-1-3 \
    libexpat1 \
    libxcb1 \
    libx11-6 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libgio-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
