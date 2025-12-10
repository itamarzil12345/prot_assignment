"""add frequent terms to analysis type enum

Revision ID: add_frequent_terms
Revises: add_category_grouping
Create Date: 2025-12-10 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_frequent_terms'
down_revision = 'add_category_grouping'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add FREQUENT_TERMS to analysistype enum."""
    # Add the new enum value to the existing enum type
    op.execute("ALTER TYPE analysistype ADD VALUE IF NOT EXISTS 'FREQUENT_TERMS'")


def downgrade() -> None:
    """Remove FREQUENT_TERMS from analysistype enum.
    
    Note: PostgreSQL does not support removing enum values directly.
    This would require recreating the enum type, which is complex and
    may require data migration. For now, we'll leave it as a no-op.
    
    # PostgreSQL doesn't support removing enum values easily
    # This would require recreating the enum and migrating data
    pass

