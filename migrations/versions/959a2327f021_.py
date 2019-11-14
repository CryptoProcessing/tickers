"""empty message

Revision ID: 959a2327f021
Revises: f5745b4beee9
Create Date: 2018-05-31 14:40:11.191252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '959a2327f021'
down_revision = 'f5745b4beee9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('markets', sa.Column('alias', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('markets', 'alias')
    # ### end Alembic commands ###