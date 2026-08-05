"""initial schema (core domain, no subscription system)

Revision ID: 0001
Revises:
Create Date: 2026-08-03

Creates the application's core tables: users, couples, albums, memories,
rituals, ritual_entries, letters, special_dates, surprises, watch_sessions,
night_sessions, refresh_tokens and audit_logs.

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.create_table(
        "couples",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("invite_code", sa.String(length=12), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=True),
        sa.Column("relationship_start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "relationship_status",
            sa.Enum("dating", "engaged", "married", name="relationshipstatus"),
            nullable=False,
        ),
        sa.Column("current_streak", sa.Integer(), nullable=False),
        sa.Column("longest_streak", sa.Integer(), nullable=False),
        sa.Column("last_activity_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cover_image_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_couples"),
    )
    op.create_index("ix_couples_id", "couples", ["id"], unique=False)
    op.create_index("ix_couples_invite_code", "couples", ["invite_code"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("current_mood", sa.String(length=30), nullable=True),
        sa.Column("mood_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_users_couple_id_couples",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_couple_id", "users", ["couple_id"], unique=False)

    op.create_table(
        "albums",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("cover_memory_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_albums"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_albums_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name="fk_albums_created_by_users",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_albums_id", "albums", ["id"], unique=False)
    op.create_index("ix_albums_created_by", "albums", ["created_by"], unique=False)
    op.create_index("ix_albums_couple_id", "albums", ["couple_id"], unique=False)
    op.create_index("ix_albums_cover_memory_id", "albums", ["cover_memory_id"], unique=False)

    op.create_table(
        "memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("album_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("memory_date", sa.Date(), nullable=True),
        sa.Column("media_url", sa.String(length=500), nullable=True),
        sa.Column("thumbnail_url", sa.String(length=500), nullable=True),
        sa.Column("media_type", sa.String(length=20), nullable=True),
        sa.Column("s3_key", sa.String(length=512), nullable=False),
        sa.Column("s3_thumbnail_key", sa.String(length=512), nullable=True),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("caption", sa.String(length=500), nullable=True),
        sa.Column(
            "category",
            sa.Enum(
                "TRAVEL",
                "ROUTINE",
                "ANNIVERSARY",
                "NATURE",
                "FOOD",
                "NIGHT",
                "SELFIE",
                "OTHER",
                name="memorycategory",
            ),
            nullable=False,
        ),
        sa.Column("file_size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_memories"),
        sa.ForeignKeyConstraint(
            ["album_id"],
            ["albums.id"],
            name="fk_memories_album_id_albums",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name="fk_memories_author_id_users",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_memories_couple_id_couples",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_memories_id", "memories", ["id"], unique=False)
    op.create_index("ix_memories_album_id", "memories", ["album_id"], unique=False)
    op.create_index("ix_memories_author_id", "memories", ["author_id"], unique=False)
    op.create_index("ix_memories_couple_id", "memories", ["couple_id"], unique=False)

    op.create_foreign_key(
        "fk_albums_cover_memory_id_memories",
        "albums",
        "memories",
        ["cover_memory_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "rituals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=False),
        sa.Column("icon", sa.String(length=10), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("current_streak", sa.Integer(), nullable=False),
        sa.Column("longest_streak", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_rituals"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_rituals_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name="fk_rituals_created_by_couples",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_rituals_id", "rituals", ["id"], unique=False)
    op.create_index("ix_rituals_couple_id", "rituals", ["couple_id"], unique=False)

    op.create_table(
        "ritual_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("ritual_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "COMPLETED", "SKIPPED", name="ritualstatus"),
            nullable=False,
        ),
        sa.Column("note", sa.String(length=300), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_ritual_entries"),
        sa.ForeignKeyConstraint(
            ["ritual_id"],
            ["rituals.id"],
            name="fk_ritual_entries_ritual_id_rituals",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_ritual_entries_user_id_users",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_ritual_entries_id", "ritual_entries", ["id"], unique=False)
    op.create_index(
        "ix_ritual_entries_ritual_date",
        "ritual_entries",
        ["ritual_id", "entry_date"],
        unique=False,
    )
    op.create_index(
        "ix_ritual_entries_user_date",
        "ritual_entries",
        ["user_id", "entry_date"],
        unique=False,
    )

    op.create_table(
        "letters",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recipient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.Enum("DRAFT", "SENT", "READ", name="letterstatus"), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_letters"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_letters_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
            name="fk_letters_author_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["users.id"],
            name="fk_letters_recipient_id_users",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_letters_id", "letters", ["id"], unique=False)
    op.create_index("ix_letters_couple_id", "letters", ["couple_id"], unique=False)
    op.create_index("ix_letters_recipient_id", "letters", ["recipient_id"], unique=False)

    op.create_table(
        "special_dates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("icon", sa.String(length=10), nullable=False),
        sa.Column("event_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_recurring_yearly", sa.Boolean(), nullable=False),
        sa.Column("notify_days_before", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_special_dates"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_special_dates_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name="fk_special_dates_created_by_users",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_special_dates_id", "special_dates", ["id"], unique=False)
    op.create_index("ix_special_dates_couple_id", "special_dates", ["couple_id"], unique=False)

    op.create_table(
        "surprises",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sender_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recipient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("surprise_type", sa.String(length=30), nullable=False),
        sa.Column("status", sa.Enum("LOCKED", "PENDING", "OPENED", "DELIVERED", name="surprisestatus"), nullable=False),
        sa.Column("unlocks_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("media_s3_key", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_surprises"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_surprises_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["users.id"],
            name="fk_surprises_sender_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["users.id"],
            name="fk_surprises_recipient_id_users",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_surprises_id", "surprises", ["id"], unique=False)
    op.create_index("ix_surprises_couple_id", "surprises", ["couple_id"], unique=False)
    op.create_index("ix_surprises_recipient_id", "surprises", ["recipient_id"], unique=False)
    op.create_index("ix_surprises_unlocks_at", "surprises", ["unlocks_at"], unique=False)

    op.create_table(
        "watch_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("initiated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("media_title", sa.String(length=200), nullable=False),
        sa.Column("media_url", sa.String(length=1000), nullable=True),
        sa.Column("media_type", sa.String(length=30), nullable=False),
        sa.Column("is_playing", sa.Boolean(), nullable=False),
        sa.Column("current_position_seconds", sa.Numeric(12, 3), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_watch_sessions"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_watch_sessions_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["initiated_by"],
            ["users.id"],
            name="fk_watch_sessions_initiated_by_users",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_watch_sessions_id", "watch_sessions", ["id"], unique=False)
    op.create_index("ix_watch_sessions_couple_id", "watch_sessions", ["couple_id"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), server_default=sa.text("'false'"), nullable=False),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_refresh_tokens"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_refresh_tokens_user_id_users",
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_refresh_tokens_id", "refresh_tokens", ["id"], unique=False)
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False)
    op.create_index("ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"], unique=True)

    op.create_table(
        "night_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.Enum("ACTIVE", "ENDED","WAITING", "WAITING_FOR_USER2", name="nightsessionstatus"), nullable=False),
        sa.Column("ambient_sound", sa.String(length=50), nullable=False),
        sa.Column("user1_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user1_joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user2_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user2_joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_night_sessions"),
        sa.ForeignKeyConstraint(
            ["couple_id"],
            ["couples.id"],
            name="fk_night_sessions_couple_id_couples",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user1_id"],
            ["users.id"],
            name="fk_night_sessions_user1_id_users",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user2_id"],
            ["users.id"],
            name="fk_night_sessions_user2_id_users",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_night_sessions_id", "night_sessions", ["id"], unique=False)
    op.create_index("ix_night_sessions_couple_id", "night_sessions", ["couple_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("couple_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=True),
        sa.Column("resource_id", sa.String(length=36), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("extra", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_audit_logs"),
    )
    op.create_index("ix_audit_logs_id", "audit_logs", ["id"], unique=False)
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"], unique=False)
    op.create_index("ix_audit_logs_couple_id", "audit_logs", ["couple_id"], unique=False)
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("night_sessions")
    op.drop_table("refresh_tokens")
    op.drop_table("watch_sessions")
    op.drop_table("surprises")
    op.drop_table("special_dates")
    op.drop_table("letters")
    op.drop_table("ritual_entries")
    op.drop_table("rituals")
    op.drop_constraint("fk_albums_cover_memory_id_memories", "albums", type_="foreignkey")
    op.drop_table("memories")
    op.drop_table("albums")
    op.drop_table("users")
    op.drop_table("couples")

    op.execute(sa.text("DROP TYPE IF EXISTS relationshipstatus"))
    op.execute(sa.text("DROP TYPE IF EXISTS memorycategory"))
    op.execute(sa.text("DROP TYPE IF EXISTS ritualstatus"))
