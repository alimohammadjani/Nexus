#!/bin/bash

# ============================================
#   DevHub — Setup Script
#   همه پیش‌نیازها رو نصب می‌کنه
# ============================================

set -e  # اگه خطا بود متوقف بشه

echo ""
echo "🚀 شروع نصب DevHub dependencies..."
echo "======================================"

# ============================================
# 1. بررسی پیش‌نیازهای سیستم
# ============================================
echo ""
echo "📋 بررسی پیش‌نیازهای سیستم..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 نصب نیست! از python.org نصب کن"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js نصب نیست! از nodejs.org نصب کن"
    exit 1
fi
echo "✅ Node.js: $(node --version)"

# npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm نصب نیست!"
    exit 1
fi
echo "✅ npm: $(npm --version)"

# Docker
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker نصب نیست — برای PostgreSQL و Redis لازمه"
    echo "   از docker.com نصب کن، بعد دوباره اجرا کن"
else
    echo "✅ Docker: $(docker --version)"
fi

# Git
if ! command -v git &> /dev/null; then
    echo "❌ Git نصب نیست!"
    exit 1
fi
echo "✅ Git: $(git --version)"

# ============================================
# 2. ساختار پوشه‌ها
# ============================================
echo ""
echo "📁 ساخت ساختار پروژه..."

mkdir -p devhub/backend
mkdir -p devhub/frontend

# ============================================
# 3. بک‌اند — Python Virtual Environment
# ============================================
echo ""
echo "🐍 راه‌اندازی Python Virtual Environment..."

cd devhub/backend

python3 -m venv venv

# activate بر اساس سیستم‌عامل
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment ساخته شد"

# ============================================
# 4. نصب پکیج‌های Python
# ============================================
echo ""
echo "📦 نصب پکیج‌های Python..."

pip install --upgrade pip --quiet

pip install \
    fastapi==0.111.0 \
    uvicorn[standard]==0.30.1 \
    sqlalchemy==2.0.30 \
    alembic==1.13.1 \
    pydantic==2.7.1 \
    pydantic-settings==2.3.0 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    celery==5.4.0 \
    redis==5.0.4 \
    python-multipart==0.0.9 \
    httpx==0.27.0 \
    boto3==1.34.0 \
    sentry-sdk[fastapi]==2.5.1 \
    resend==0.8.0 \
    stripe==9.12.0 \
    psycopg2-binary==2.9.9 \
    pytest==8.2.2 \
    pytest-asyncio==0.23.7 \
    pytest-cov==5.0.0 \
    python-dotenv==1.0.1

echo "✅ پکیج‌های Python نصب شدن"

# ساخت requirements.txt
pip freeze > requirements.txt
echo "✅ requirements.txt ساخته شد"

# ساخت .env.example
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/devhub

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3 / Cloudflare R2
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_BUCKET_NAME=devhub-files
AWS_REGION=us-east-1

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Resend (Email)
RESEND_API_KEY=re_...

# Sentry
SENTRY_DSN=https://...

# App
APP_NAME=DevHub
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
EOF

echo "✅ .env.example ساخته شد"

# برگشت به ریشه
cd ../..

# ============================================
# 5. فرانت‌اند — React + TypeScript
# ============================================
echo ""
echo "⚛️  ساخت پروژه React با Vite..."

cd devhub/frontend

# ساخت پروژه React با TypeScript
npm create vite@latest . -- --template react-ts --yes 2>/dev/null || true

echo ""
echo "📦 نصب پکیج‌های فرانت‌اند..."

# نصب پکیج‌های اصلی
npm install \
    @tanstack/react-query \
    axios \
    zustand \
    react-router-dom \
    react-hook-form \
    @hookform/resolvers \
    zod \
    clsx \
    tailwind-merge \
    lucide-react \
    @stripe/stripe-js \
    @stripe/react-stripe-js \
    @sentry/react \
    --silent

# نصب devDependencies
npm install -D \
    tailwindcss \
    postcss \
    autoprefixer \
    @types/node \
    --silent

# راه‌اندازی Tailwind
npx tailwindcss init -p --quiet 2>/dev/null || true

echo "✅ پکیج‌های فرانت‌اند نصب شدن"

# ساخت .env.example
cat > .env.example << 'EOF'
VITE_API_URL=http://localhost:8000/api/v1
VITE_STRIPE_PUBLIC_KEY=pk_test_...
VITE_SENTRY_DSN=https://...
EOF

echo "✅ .env.example فرانت ساخته شد"

cd ../..

# ============================================
# 6. Docker Compose
# ============================================
echo ""
echo "🐳 ساخت docker-compose.yml..."

cat > devhub/docker-compose.yml << 'EOF'
version: '3.9'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: devhub
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: ./backend/.env
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  celery:
    build: ./backend
    env_file: ./backend/.env
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    command: celery -A app.tasks worker --loglevel=info

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
EOF

echo "✅ docker-compose.yml ساخته شد"

# ============================================
# 7. راه‌اندازی PostgreSQL و Redis با Docker
# ============================================
echo ""
echo "🐳 راه‌اندازی PostgreSQL و Redis..."

cd devhub
docker compose up -d db redis 2>/dev/null && echo "✅ PostgreSQL و Redis در حال اجرا هستن" || echo "⚠️  Docker نصب نیست، PostgreSQL و Redis رو دستی نصب کن"
cd ..

# ============================================
# 8. نمایش خلاصه
# ============================================
echo ""
echo "======================================"
echo "✅ همه چیز آماده‌ست!"
echo "======================================"
echo ""
echo "📌 قدم‌های بعدی:"
echo ""
echo "  1. کپی .env:"
echo "     cp devhub/backend/.env.example devhub/backend/.env"
echo "     cp devhub/frontend/.env.example devhub/frontend/.env"
echo ""
echo "  2. اجرای بک‌اند:"
echo "     cd devhub/backend"
echo "     source venv/bin/activate   (Mac/Linux)"
echo "     venv\\Scripts\\activate      (Windows)"
echo "     uvicorn app.main:app --reload"
echo ""
echo "  3. اجرای فرانت‌اند:"
echo "     cd devhub/frontend"
echo "     npm run dev"
echo ""
echo "  4. داک FastAPI:"
echo "     http://localhost:8000/docs"
echo ""
echo "  5. فرانت‌اند:"
echo "     http://localhost:3000"
echo ""
echo "🚀 DevHub آماده توسعه‌ست!"
