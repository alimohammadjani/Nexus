"""Seed demo data on first startup."""

import logging

from sqlalchemy import select

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.job import Job
from app.models.learning import Course, CourseEnrollment, Lesson, Roadmap, RoadmapStage
from app.models.market import Order, Product
from app.models.payment import Payment, Transaction
from app.models.user import Skill, User

logger = logging.getLogger("devhub.seed")


def seed_demo_data() -> None:
    """Idempotently insert demo rows when the database is empty."""
    db = SessionLocal()
    try:
        if db.scalar(select(User).limit(1)):
            return

        # Users
        dev = User(
            email="demo@devhub.app",
            full_name="Sara Mohammadi",
            password_hash=hash_password("demo12345"),
            role="developer",
            bio="Frontend developer focused on React and TypeScript.",
            is_verified=True,
        )
        employer = User(
            email="employer@devhub.app",
            full_name="Nova Fintech",
            password_hash=hash_password("demo12345"),
            role="employer",
            is_employer=True,
            company="Nova Fintech",
        )
        admin = User(
            email="admin@devhub.app",
            full_name="DevHub Admin",
            password_hash=hash_password("demo12345"),
            role="admin",
            is_verified=True,
        )
        db.add_all([dev, employer, admin])
        db.flush()

        db.add_all(
            [
                Skill(user_id=dev.id, name="React", level="intermediate"),
                Skill(user_id=dev.id, name="TypeScript", level="intermediate"),
                Skill(user_id=dev.id, name="Python", level="beginner"),
                Skill(user_id=employer.id, name="DevOps", level="expert"),
            ]
        )

        # Jobs
        job1 = Job(
            owner_id=employer.id,
            title="Frontend Developer (React / TypeScript)",
            company="Nova Fintech",
            description="Build and maintain modern React applications with a focus on performance and UX.",
            location="Tehran / Remote",
            type="full_time",
            mode="remote",
            level="mid",
            salary_range="30,000,000 - 50,000,000 T",
            skills="React,TypeScript,Next.js",
            is_featured=True,
            budget=200000,
        )
        job2 = Job(
            owner_id=employer.id,
            title="Backend Engineer (FastAPI / PostgreSQL)",
            company="Abree Cloud",
            description="Design robust APIs and data models for a SaaS platform.",
            location="Remote",
            type="full_time",
            mode="hybrid",
            level="senior",
            salary_range="50,000,000 - 70,000,000 T",
            skills="Python,FastAPI,PostgreSQL,Docker",
            is_featured=True,
            budget=350000,
        )
        job3 = Job(
            owner_id=dev.id,
            title="Build a landing page",
            company="Freelance",
            description="A static landing page for a startup.",
            location="Remote",
            type="freelance",
            mode="remote",
            level="junior",
            skills="HTML,CSS,React",
            budget=18000000,
        )
        db.add_all([job1, job2, job3])
        db.flush()

        # Roadmaps
        roadmap = Roadmap(
            title="Backend Developer",
            subtitle="API, database, security and services architecture",
            description="Complete backend path from Python basics to production deployments.",
            category="backend",
            color="#0ea5e9",
        )
        db.add(roadmap)
        db.flush()
        db.add_all(
            [
                RoadmapStage(
                    roadmap_id=roadmap.id,
                    order=1,
                    title="Python / Node Basics",
                    description="Learn the language fundamentals.",
                    resources="MDN, Official docs",
                    project="Build a CLI tool",
                    checkpoint="Run unit tests",
                ),
                RoadmapStage(
                    roadmap_id=roadmap.id,
                    order=2,
                    title="REST API",
                    description="Design and build RESTful endpoints.",
                    resources="FastAPI Docs",
                    project="Inventory API",
                    checkpoint="OpenAPI review",
                ),
                RoadmapStage(
                    roadmap_id=roadmap.id,
                    order=3,
                    title="PostgreSQL",
                    description="Model relational data and optimize queries.",
                    resources="PostgreSQL Tutorial",
                    project="E-commerce schema",
                    checkpoint="Index review",
                ),
                RoadmapStage(
                    roadmap_id=roadmap.id,
                    order=4,
                    title="Auth and Deploy",
                    description="Secure the API and ship it to production.",
                    resources="Docker, GitHub Actions",
                    project="Deploy production service",
                    checkpoint="Security audit",
                ),
            ]
        )

        # Courses
        course = Course(
            title="FastAPI Crash Course",
            description="Learn to build a complete REST API with FastAPI, SQLAlchemy and Pydantic.",
            category="backend",
            level="beginner",
            instructor_name="DevHub Team",
            is_free=True,
            duration_hours=6,
        )
        db.add(course)
        db.flush()
        db.add_all(
            [
                Lesson(course_id=course.id, order=1, title="Setup", content="Install dependencies and run the server.", duration_minutes=20),
                Lesson(course_id=course.id, order=2, title="Models & schemas", content="Define ORM models and Pydantic schemas.", duration_minutes=40),
                Lesson(course_id=course.id, order=3, title="Auth", content="Protect endpoints with JWT.", duration_minutes=45),
            ]
        )
        db.add(CourseEnrollment(course_id=course.id, user_id=dev.id, progress=0.5))

        # Marketplace
        product1 = Product(
            seller_id=dev.id,
            title="Persian SaaS Dashboard Template",
            description="A modern responsive dashboard template built with React and Tailwind CSS.",
            category="template",
            price=1290000,
            currency="IRR",
            tags="react,typescript,dashboard",
            rating=4.9,
            sales=240,
        )
        product2 = Product(
            seller_id=dev.id,
            title="Ready-to-use OTP API",
            description="Production-ready OTP verification API with rate limiting.",
            category="api",
            price=390000,
            currency="IRR",
            tags="otp,api,verification",
            rating=4.8,
            sales=480,
        )
        product3 = Product(
            seller_id=employer.id,
            title="Developer Resume Plugin",
            description="A plugin that generates a developer portfolio from a GitHub profile.",
            category="plugin",
            price=790000,
            currency="IRR",
            tags="plugin,resume,portfolio",
            rating=4.7,
            sales=112,
        )
        db.add_all([product1, product2, product3])
        db.flush()
        db.add(Order(product_id=product1.id, buyer_id=employer.id, amount=product1.price, currency="IRR", status="paid"))

        # Payments
        tx = Transaction(
            user_id=dev.id,
            amount=100,
            currency="USD",
            status="succeeded",
            provider="stripe",
            reference="demo_tx_001",
            description="Demo transaction",
        )
        db.add(tx)
        db.flush()
        db.add(Payment(transaction_id=tx.id, method="card", paid_at=tx.created_at))

        db.commit()
        logger.info("Seeded demo data for DevHub")
    finally:
        db.close()
