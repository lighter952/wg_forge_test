"""Create tables: cats, users, user_passwords

Revision ID: fe226ad9fc8f
Revises: 
Create Date: 2023-08-15 13:26:14.703630

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fe226ad9fc8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cats',
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('color', postgresql.ENUM('black', 'white', 'black & white', 'red', 'red & white', 'red & black & white', name='cats_colors_enum'), nullable=True),
    sa.Column('tail_length', sa.Integer(), nullable=True),
    sa.Column('whiskers_length', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('username', sa.VARCHAR(length=100), nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_passwords',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=100), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_user_passwords_user_id'), 'user_passwords', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_passwords_user_id'), table_name='user_passwords')
    op.drop_table('user_passwords')
    op.drop_table('users')
    op.drop_table('cats')
    # ### end Alembic commands ###
