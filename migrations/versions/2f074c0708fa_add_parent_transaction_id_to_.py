"""Add parent_transaction_id to transactions

Revision ID: 2f074c0708fa
Revises: 
Create Date: 2025-05-25 16:07:23.820232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '2f074c0708fa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'transactions_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('type', sa.String(10), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('payee', sa.String(), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id')),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id')),
        sa.Column('parent_transaction_id', sa.Integer(), sa.ForeignKey('transactions.id'))
    )

    op.execute("""
        INSERT INTO transactions_new (
            id, type, date, amount, payee, category_id, tag_id
        )
        SELECT id, type, date, amount, payee, category_id, tag_id FROM transactions
    """)

    op.drop_table('transactions')

    op.rename_table('transactions_new', 'transactions')


def downgrade():
    op.create_table(
        'transactions_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('type', sa.String(10), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('payee', sa.String(), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id')),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id'))
    )

    op.execute("""
        INSERT INTO transactions_old (
            id, type, date, amount, payee, category_id, tag_id
        )
        SELECT id, type, date, amount, payee, category_id, tag_id FROM transactions
    """)

    op.drop_table('transactions')
    op.rename_table('transactions_old', 'transactions')
