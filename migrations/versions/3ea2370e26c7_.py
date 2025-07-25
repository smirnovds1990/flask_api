"""empty message

Revision ID: 3ea2370e26c7
Revises: 1a2058bb2f55
Create Date: 2025-07-21 12:50:48.205546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ea2370e26c7'
down_revision = '1a2058bb2f55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('on_main', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(length=1024), nullable=False),
    sa.Column('main_image', sa.Boolean(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chosen', sa.Boolean(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('extra_field_color', sa.String(), nullable=True),
    sa.Column('extra_field_image', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('old_price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('parameter_string', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_marks_relations',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('mark_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mark_id'], ['product_marks.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'mark_id')
    )
    op.create_table('products_categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('category_id', 'product_id')
    )
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('sort_order',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('sort_order',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.drop_table('products_categories')
    op.drop_table('product_marks_relations')
    op.drop_table('parameters')
    op.drop_table('images')
    op.drop_table('products')
    # ### end Alembic commands ###
