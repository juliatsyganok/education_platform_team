from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UGCItem(db.Model):
    """
    Модель для хранения контента от ползователя
    """
    __tablename__ = "ugc_items"
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(
        db.String(50),
        nullable=False
    )
    object_id = db.Column(
        db.Integer,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    rating = db.Column(
        db.Integer,
        nullable=True
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "object_type": self.object_type,
            "object_id": self.object_id,
            "user_id": self.user_id,
            "content": self.content,
            "rating": self.rating,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<UGCItem id={self.id} type={self.object_type} object={self.object_id}>"