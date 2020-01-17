"""empty message

Revision ID: b9ba05e42e75
Revises: 
Create Date: 2020-01-17 21:05:28.647126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ba05e42e75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_goal_goal', table_name='goal')
    op.drop_table('goal')
    op.drop_index('ix_tutors_name', table_name='tutors')
    op.drop_table('tutors')
    op.drop_table('tutors_goals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tutors_goals',
    sa.Column('tutor_id', sa.INTEGER(), nullable=True),
    sa.Column('goal_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goal.id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutor.id'], )
    )
    op.create_table('tutors',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('about', sa.VARCHAR(length=500), nullable=True),
    sa.Column('rating', sa.FLOAT(), nullable=True),
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tutors_name', 'tutors', ['name'], unique=1)
    op.create_table('goal',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('goal', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_goal_goal', 'goal', ['goal'], unique=1)
    # ### end Alembic commands ###