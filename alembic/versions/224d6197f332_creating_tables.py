"""Creating tables

Revision ID: 224d6197f332
Revises: 
Create Date: 2024-01-02 14:57:14.981817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '224d6197f332'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('extract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['map.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('primary_phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.Column('processingCompleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['map.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('town',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['map.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('primary_phase_id', sa.Integer(), nullable=False),
    sa.Column('phase_number', sa.Integer(), nullable=False),
    sa.Column('towns', sa.String(length=16), nullable=False),
    sa.Column('processingCompleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['primary_phase_id'], ['primary_phase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phase')
    op.drop_table('town')
    op.drop_table('primary_phase')
    op.drop_table('image')
    op.drop_table('extract')
    op.drop_table('user')
    op.drop_table('map')
    # ### end Alembic commands ###