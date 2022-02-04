"""First Migration

Revision ID: fe4c2cc62447
Revises: 
Create Date: 2022-02-04 16:50:08.337599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe4c2cc62447'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_project_summary', table_name='project')
    op.drop_index('ix_project_title', table_name='project')
    op.drop_table('project')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_token', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('token', sa.VARCHAR(length=32), nullable=True),
    sa.Column('token_expiration', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.create_index('ix_user_token', 'user', ['token'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.create_table('project',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=True),
    sa.Column('summary', sa.VARCHAR(length=255), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('start_time', sa.DATETIME(), nullable=True),
    sa.Column('end_time', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_title', 'project', ['title'], unique=False)
    op.create_index('ix_project_summary', 'project', ['summary'], unique=False)
    # ### end Alembic commands ###
