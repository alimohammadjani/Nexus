# app/database.py
# ============================================
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# app/models/base.py
# ============================================
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# app/models/user.py
# ============================================
import enum
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    STUDENT = "student"        # دانشجو/برنامه‌نویس
    COMPANY = "company"        # شرکت / کارفرما
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # روابط
    progress = relationship("RoadmapProgress", back_populates="user")
    portfolio_projects = relationship("PortfolioProject", back_populates="user")
    job_posts = relationship("JobPost", back_populates="poster")
    applications = relationship("JobApplication", back_populates="applicant")
    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="buyer")


# ============================================
# app/models/roadmap.py
# ============================================
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Roadmap(BaseModel):
    """مثلاً: Frontend Developer, Backend Developer, DevOps"""
    __tablename__ = "roadmaps"

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)       # frontend, backend, devops, mobile
    description = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)

    steps = relationship("RoadmapStep", back_populates="roadmap", order_by="RoadmapStep.order_index")


class RoadmapStep(BaseModel):
    """هر مرحله از roadmap - مثلاً HTML/CSS, JavaScript, React"""
    __tablename__ = "roadmap_steps"

    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmaps.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)     # ترتیب نمایش
    resources = Column(Text, nullable=True)           # JSON: لینک منابع رایگان
    project_prompt = Column(Text, nullable=True)       # پروژه عملی این مرحله

    roadmap = relationship("Roadmap", back_populates="steps")
    progress_entries = relationship("RoadmapProgress", back_populates="step")


class RoadmapProgress(BaseModel):
    """پیشرفت هر کاربر روی هر مرحله"""
    __tablename__ = "roadmap_progress"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey("roadmap_steps.id"), nullable=False)
    completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="progress")
    step = relationship("RoadmapStep", back_populates="progress_entries")


# ============================================
# app/models/portfolio.py
# ============================================
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class PortfolioProject(BaseModel):
    """پروژه‌های تکمیل‌شده کاربر - خودکار از roadmap یا دستی اضافه‌شده"""
    __tablename__ = "portfolio_projects"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    user = relationship("User", back_populates="portfolio_projects")


# ============================================
# app/models/job.py
# ============================================
import enum
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class JobType(str, enum.Enum):
    PAID = "paid"              # پروژه پولی
    COLLABORATION = "collab"   # همکاری رایگان
    FULL_TIME = "full_time"    # استخدام تمام‌وقت (شرکت‌ها)


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class JobPost(BaseModel):
    """آگهی کار - چه پروژه پولی/رایگان، چه استخدام شرکت"""
    __tablename__ = "job_posts"

    poster_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(JobType), nullable=False)
    budget = Column(Numeric(10, 2), nullable=True)   # فقط برای پروژه‌های پولی
    required_skills = Column(String, nullable=True)   # comma-separated یا JSON
    location = Column(String, nullable=True)           # remote / on-site
    is_active = Column(String, default=True)

    poster = relationship("User", back_populates="job_posts")
    applications = relationship("JobApplication", back_populates="job")


class JobApplication(BaseModel):
    """درخواست برای یک آگهی"""
    __tablename__ = "job_applications"

    job_id = Column(UUID(as_uuid=True), ForeignKey("job_posts.id"), nullable=False)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    cover_letter = Column(Text, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)

    job = relationship("JobPost", back_populates="applications")
    applicant = relationship("User", back_populates="applications")


# ============================================
# app/models/market.py
# ============================================
import enum
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    DELIVERED = "delivered"
    REFUNDED = "refunded"


class Product(BaseModel):
    """محصول در مارکت - کد، قالب، پلاگین، اسکریپت"""
    __tablename__ = "products"

    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String, nullable=False)      # template, plugin, script, api
    file_url = Column(String, nullable=False)        # لینک فایل در S3/R2
    preview_image = Column(String, nullable=True)
    downloads_count = Column(Integer, default=0)

    seller = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product")


class Order(BaseModel):
    """خرید یک محصول"""
    __tablename__ = "orders"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    commission = Column(Numeric(10, 2), nullable=False)   # سهم سایت (۱۵-۲۰٪)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_provider = Column(String, nullable=True)       # zarinpal / stripe
    payment_ref = Column(String, nullable=True)

    product = relationship("Product", back_populates="orders")
    buyer = relationship("User", back_populates="orders")
