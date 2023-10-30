"""test relation

Revision ID: e55fa0da12ba
Revises: a49d2b423974
Create Date: 2023-10-25 16:10:37.015302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e55fa0da12ba'
down_revision: Union[str, None] = 'a49d2b423974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TransportType')
    op.drop_table('Color')
    op.drop_table('TransportModel')
    op.alter_column('Transport', 'ownerId',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('Transport_transportModelId_fkey', 'Transport', type_='foreignkey')
    op.drop_constraint('Transport_colorId_fkey', 'Transport', type_='foreignkey')
    op.drop_constraint('Transport_transportTypeId_fkey', 'Transport', type_='foreignkey')
    op.drop_column('Transport', 'transportModelId')
    op.drop_column('Transport', 'colorId')
    op.drop_column('Transport', 'transportTypeId')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Transport', sa.Column('transportTypeId', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Transport', sa.Column('colorId', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Transport', sa.Column('transportModelId', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Transport_transportTypeId_fkey', 'Transport', 'TransportType', ['transportTypeId'], ['id'])
    op.create_foreign_key('Transport_colorId_fkey', 'Transport', 'Color', ['colorId'], ['id'])
    op.create_foreign_key('Transport_transportModelId_fkey', 'Transport', 'TransportModel', ['transportModelId'], ['id'])
    op.alter_column('Transport', 'ownerId',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_table('TransportModel',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"TransportModel_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='TransportModel_pkey')
    )
    op.create_table('Color',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Color_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Color_pkey')
    )
    op.create_table('TransportType',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"TransportType_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='TransportType_pkey')
    )
    # ### end Alembic commands ###