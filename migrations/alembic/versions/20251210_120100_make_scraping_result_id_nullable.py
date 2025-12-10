"""make scraping_result_id nullable for global aggregations

Revision ID: make_scraping_result_id_nullable
Revises: add_frequent_terms
Create Date: 2025-12-10 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'make_scraping_result_id_nullable'
down_revision = 'add_frequent_terms'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Make scraping_result_id nullable to support global aggregations like FREQUENT_TERMS."""
    op.alter_column(
        'analysis_results',
        'scraping_result_id',
        existing_type=sa.UUID(),
        nullable=True
    )


def downgrade() -> None:
    """Make scraping_result_id NOT NULL again.
    
    Note: This will fail if there are any NULL values in the column.
    """
    op.alter_column(
        'analysis_results',
        'scraping_result_id',
        existing_type=sa.UUID(),
        nullable=False
    )

