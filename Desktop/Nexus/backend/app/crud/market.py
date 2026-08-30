"""Marketplace CRUD helpers."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.market import Order, Product, ProductReview
from app.schemas.market import ProductCreate, ProductUpdate, ReviewCreate


def list_products(
    db: Session,
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Product]:
    stmt = select(Product).where(Product.is_published.is_(True))
    if category:
        stmt = stmt.where(Product.category == category)
    if search:
        stmt = stmt.where(Product.title.ilike(f"%{search}%") | Product.description.ilike(f"%{search}%"))
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    stmt = stmt.order_by(Product.rating.desc(), Product.sales.desc())
    return list(db.scalars(stmt))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def create_product(db: Session, seller_id: int, data: ProductCreate) -> Product:
    product = Product(seller_id=seller_id, **data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def add_review(db: Session, product: Product, user_id: int, data: ReviewCreate) -> ProductReview:
    review = db.scalar(
        select(ProductReview).where(
            ProductReview.product_id == product.id, ProductReview.user_id == user_id
        )
    )
    if not review:
        review = ProductReview(product_id=product.id, user_id=user_id)
        db.add(review)
    review.rating = data.rating
    review.comment = data.comment
    db.flush()
    avg = db.scalar(
        select(func.avg(ProductReview.rating)).where(ProductReview.product_id == product.id)
    )
    product.rating = round(float(avg or 0), 1)
    db.commit()
    db.refresh(review)
    return review


def create_order(db: Session, product: Product, buyer_id: int, status: str = "paid") -> Order:
    order = Order(
        product_id=product.id,
        buyer_id=buyer_id,
        amount=product.price,
        currency=product.currency,
        status=status,
    )
    product.sales += 1
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
