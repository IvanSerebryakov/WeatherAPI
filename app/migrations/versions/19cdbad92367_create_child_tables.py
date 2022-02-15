"""create child tables

Revision ID: 19cdbad92367
Revises: 5b35cabeb899
Create Date: 2022-02-15 08:47:47.152683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19cdbad92367'
down_revision = '5b35cabeb899'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('day_feels_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('morn', sa.Float(), nullable=True),
    sa.Column('day', sa.Float(), nullable=True),
    sa.Column('eve', sa.Float(), nullable=True),
    sa.Column('night', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['public.day_data.day_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('day_temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('morn', sa.Float(), nullable=True),
    sa.Column('day', sa.Float(), nullable=True),
    sa.Column('day_min', sa.Float(), nullable=True),
    sa.Column('day_max', sa.Float(), nullable=True),
    sa.Column('eve', sa.Float(), nullable=True),
    sa.Column('night', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['public.day_data.day_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('day_weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('weather_id', sa.Integer(), nullable=True),
    sa.Column('main', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['public.day_data.day_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('hour_weather',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hour_id', sa.Integer(), nullable=False),
    sa.Column('weather_id', sa.Integer(), nullable=True),
    sa.Column('main', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['hour_id'], ['public.hour_data.hour_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hour_weather', schema='public')
    op.drop_table('day_weather', schema='public')
    op.drop_table('day_temperature', schema='public')
    op.drop_table('day_feels_like', schema='public')
    # ### end Alembic commands ###
