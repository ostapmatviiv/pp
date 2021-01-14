"""create account table

Revision ID: b303113dc8f4
Revises: 
Create Date: 2020-12-13 16:11:42.390125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b303113dc8f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
    'user',
    sa.Column("user_id", sa.Integer, primary_key=True),
    sa.Column('username', sa.String, unique=True),
    sa.Column('password',sa.String,unique=True)
    )


    op.create_table(
    'item',
    sa.Column("name", sa.String, unique=True),
    sa.Column('item_id', sa.Integer, primary_key=True),
    sa.Column('quantity', sa.Integer),
    sa.Column('price',sa.String,unique=True),
    sa.Column('describe',sa.String,unique=True)
    )

    op.create_table(
        'provisor',
        sa.Column("provisor_id", sa.Integer, primary_key=True),
        sa.Column('provisorname', sa.String, unique=True),
        sa.Column('provisorpass', sa.String,unique=True)
    )

    op.create_table(
        'order',
        sa.Column('order_id',sa.Integer, primary_key=True),
        sa.Column('order_user_id',sa.Integer),
        sa.Column('order_item_id',sa.Integer),
        sa.Column('quantity_in_order',sa.Integer)
    )

    op.create_table(
        'order_demand',
        sa.Column('order_demand_id', sa.Integer, primary_key=True),
        sa.Column('order_demand_user_id', sa.Integer),
        sa.Column('order_demand_item_id', sa.Integer),
        sa.Column('quantity_in_order_demand', sa.Integer)
    )

def downgrade():
    op.drop_table('user')
    op.drop_table('item')
    op.drop_table('provisor')
    op.drop_table('order')
    op.drop_table('order_demand')
