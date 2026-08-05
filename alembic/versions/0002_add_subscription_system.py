"""add subscription system (plans, subscriptions, subscription events)

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-05

Adds the subscription/billing system introduced after the initial schema:

- New native enum types: ``plantier``, ``billinginterval``,
  ``subscriptionstatus``
- New columns on ``couples``: ``subscription_status``,
  ``subscription_expires_at``
- New column on ``users``: ``stripe_customer_id``
- New tables: ``plans``, ``subscriptions``, ``subscription_events``

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    plantier = postgresql.ENUM(
        "FREE",
        "PREMIUM",
        name="plantier",
        create_type=False,
    )
    billinginterval = postgresql.ENUM(
        "MONTHLY",
        "YEARLY",
        name="billinginterval",
        create_type=False,
    )
    subscriptionstatus = postgresql.ENUM(
        "TRIALING",
        "ACTIVE",
        "PAST_DUE",
        "CANCELED",
        "UNPAID",
        "INCOMPLETE",
        name="subscriptionstatus",
        create_type=False,
    )

    sa.Enum("FREE", "PREMIUM", name="plantier").create(op.get_bind(), checkfirst=True)
    sa.Enum("MONTHLY", "YEARLY", name="billinginterval").create(
        op.get_bind(), checkfirst=True
    )
    sa.Enum(
        "TRIALING",
        "ACTIVE",
        "PAST_DUE",
        "CANCELED",
        "UNPAID",
        "INCOMPLETE",
        name="subscriptionstatus",
    ).create(op.get_bind(), checkfirst=True)

    op.add_column(
        "couples",
        sa.Column(
            "subscription_status",
            subscriptionstatus,
            server_default=sa.text("'ACTIVE'"),
            nullable=False,
        ),
    )
    op.alter_column("couples", "subscription_status", server_default=None)
    op.add_column(
        "couples",
        sa.Column("subscription_expires_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.add_column(
        "users",
        sa.Column("stripe_customer_id", sa.String(length=64), nullable=True),
    )
    op.create_unique_constraint(
        "uq_users_stripe_customer_id", "users", ["stripe_customer_id"]
    )

    op.create_table(
        "plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("tier", plantier, nullable=False),
        sa.Column("billing_interval", billinginterval, nullable=True),
        sa.Column("stripe_price_id", sa.String(length=64), nullable=True),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("max_albums", sa.Integer(), nullable=True),
        sa.Column("max_album_photos", sa.Integer(), nullable=True),
        sa.Column("max_rituals", sa.Integer(), nullable=True),
        sa.Column("can_use_night_together", sa.Boolean(), nullable=False),
        sa.Column("can_use_watch_together", sa.Boolean(), nullable=False),
        sa.Column("can_send_surprises", sa.Boolean(), nullable=False),
        sa.Column("can_write_letters", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_plans"),
        sa.UniqueConstraint("tier", "billing_interval", name="uq_plan_tier_interval"),
        sa.UniqueConstraint("stripe_price_id", name="uq_plans_stripe_price_id"),
    )
    op.create_index("ix_plans_id", "plans", ["id"], unique=False)
    op.create_index("ix_plans_tier", "plans", ["tier"], unique=False)

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stripe_subscription_id", sa.String(length=64), nullable=True),
        sa.Column("stripe_customer_id", sa.String(length=64), nullable=True),
        sa.Column("status", subscriptionstatus, nullable=False),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("trial_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("canceled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_at_period_end", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_subscriptions"),
        sa.UniqueConstraint(
            "stripe_subscription_id", name="uq_subscriptions_stripe_subscription_id"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_subscriptions_user_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["plans.id"],
            name="fk_subscriptions_plan_id_plans",
            ondelete="RESTRICT",
        ),
    )
    op.create_index("ix_subscriptions_id", "subscriptions", ["id"], unique=False)
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"], unique=False)
    op.create_index(
        "ix_subscriptions_stripe_subscription_id",
        "subscriptions",
        ["stripe_subscription_id"],
        unique=True,
    )
    op.create_index("ix_subscriptions_status", "subscriptions", ["status"], unique=False)

    op.create_table(
        "subscription_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("stripe_event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("stripe_subscription_id", sa.String(length=64), nullable=True),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("processed", sa.Boolean(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_subscription_events"),
        sa.UniqueConstraint(
            "stripe_event_id", name="uq_subscription_events_stripe_event_id"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_subscription_events_user_id_users",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_subscription_events_id", "subscription_events", ["id"], unique=False)
    op.create_index(
        "ix_sub_events_stripe_event_id",
        "subscription_events",
        ["stripe_event_id"],
        unique=True,
    )
    op.create_index("ix_sub_events_user_id", "subscription_events", ["user_id"], unique=False)
    op.create_index("ix_sub_events_created_at", "subscription_events", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_table("subscription_events")
    op.drop_table("subscriptions")
    op.drop_table("plans")

    op.drop_constraint("uq_users_stripe_customer_id", "users", type_="unique")
    op.drop_column("users", "stripe_customer_id")

    op.drop_column("couples", "subscription_expires_at")
    op.drop_column("couples", "subscription_status")

    sa.Enum("FREE", "PREMIUM", name="plantier").drop(op.get_bind(), checkfirst=True)
    sa.Enum("MONTHLY", "YEARLY", name="billinginterval").drop(
        op.get_bind(), checkfirst=True
    )
    sa.Enum(
        "TRIALING",
        "ACTIVE",
        "PAST_DUE",
        "CANCELED",
        "UNPAID",
        "INCOMPLETE",
        name="subscriptionstatus",
    ).drop(op.get_bind(), checkfirst=True)
