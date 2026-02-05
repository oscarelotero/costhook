import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class ProviderType(enum.StrEnum):
    SUPABASE = "supabase"
    VERCEL = "vercel"
    RESEND = "resend"
    STRIPE = "stripe"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class ProviderStatus(enum.StrEnum):
    CONNECTED = "connected"
    ERROR = "error"
    SYNCING = "syncing"
    PENDING = "pending"


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ProviderType] = mapped_column(Enum(ProviderType), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Encrypted JSON containing API keys and other credentials
    credentials_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ProviderStatus] = mapped_column(
        Enum(ProviderStatus), default=ProviderStatus.PENDING
    )
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    cost_records: Mapped[list["CostRecord"]] = relationship(
        "CostRecord", back_populates="provider", cascade="all, delete-orphan"
    )


class CostRecord(Base):
    __tablename__ = "cost_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("providers.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    service: Mapped[str] = mapped_column(String(100), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Additional data from the provider (JSON stored as text)
    metadata_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    provider: Mapped["Provider"] = relationship("Provider", back_populates="cost_records")
