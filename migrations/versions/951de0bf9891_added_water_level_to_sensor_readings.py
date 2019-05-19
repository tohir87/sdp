"""added water level to sensor readings

Revision ID: 951de0bf9891
Revises: 9b4c6ff76b5e
Create Date: 2019-05-19 17:46:36.215469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '951de0bf9891'
down_revision = '9b4c6ff76b5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dht_sensor_readings', sa.Column('water_level', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dht_sensor_readings', 'water_level')
    # ### end Alembic commands ###
