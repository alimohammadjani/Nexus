# DevHub

DevHub پلتفرم یکپارچه‌ای برای توسعه‌دهندگان است که یادگیری رایگان، پورتفولیوی واقعی، فرصت‌های کاری، استخدام نیرو و مارکت ابزار را در یک محصول به هم متصل می‌کند.

## ساختار

```
backend/    FastAPI backend
frontend/   React + TypeScript + Vite frontend
docker-compose.yml       Production stack
docker-compose.dev.yml   Development stack
```

## اجرای سریع

### Docker (recommended)

```bash
cp .env.example .env
make up
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- UI: http://localhost:3000

### Local development

```bash
make api      # backend on :8000 in another terminal
make web      # frontend on :5173
```

Backend seeds demo data on first run:

- demo@devhub.app / demo12345
- employer@devhub.app / demo12345
- admin@devhub.app / demo12345

## Backend capabilities

- JWT auth / register / login / me
- User profiles and skills
- Job board (CRUD, applications)
- Learning roadmaps and courses (lessons, enrollments, progress)
- Marketplace (products, reviews, orders)
- Payments (transactions, payment creation)
- SQLite by default, PostgreSQL via `DATABASE_URL`
- Alembic migrations, tests (`make test`)

## Frontend pages

- Home / marketing landing
- Login / Register
- Jobs list, job detail, post job
- Learning roadmaps, course detail, progress
- Market list, product detail, sell product
- Profile and portfolio

## Configuration

Copy `backend/.env.example` to `backend/.env` and set:

- `SECRET_KEY`
- `DATABASE_URL`
- `ALLOWED_ORIGINS`
- optional `RESEND_API_KEY`, `AWS_ACCESS_KEY_ID`, `STRIPE_SECRET_KEY`, `SENTRY_DSN`
