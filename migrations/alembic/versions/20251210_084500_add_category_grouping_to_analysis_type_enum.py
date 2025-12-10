"""add category grouping to analysis type enum

Revision ID: add_category_grouping
Revises: 
Create Date: 2025-12-10 08:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_category_grouping'
down_revision = None  # Will be set to the latest revision when running
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add CATEGORY_GROUPING to analysistype enum."""
    # Add the new enum value to the existing enum type
    op.execute("ALTER TYPE analysistype ADD VALUE IF NOT EXISTS 'CATEGORY_GROUPING'")


def downgrade() -> None:
    """Remove CATEGORY_GROUPING from analysistype enum.
    
    Note: PostgreSQL does not support removing enum values directly.
    This would require recreating the enum type, which is complex and
    may require data migration. For now, we'll leave it as a no-op.
    """
    # PostgreSQL doesn't support removing enum values easily
    # This would require recreating the enum and migrating data
    pass

