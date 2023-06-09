"""remove the test column in table user

Revision ID: 6dfa6c53d5e5
Revises: 6147cb7989a3
Create Date: 2023-06-07 23:31:07.358086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dfa6c53d5e5'
down_revision = '6147cb7989a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isActive')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isActive', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
