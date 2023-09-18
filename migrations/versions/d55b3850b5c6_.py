"""empty message

Revision ID: d55b3850b5c6
Revises: 3ef4a1afa7c6
Create Date: 2023-09-18 10:28:31.738896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd55b3850b5c6'
down_revision = '3ef4a1afa7c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_order_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('order_product_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'product_order', ['product_order_id'], ['id'])
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('order_product_id_fkey', 'product', ['product_id'], ['id'])
        batch_op.drop_column('product_order_id')

    op.drop_table('product_order')
    # ### end Alembic commands ###
