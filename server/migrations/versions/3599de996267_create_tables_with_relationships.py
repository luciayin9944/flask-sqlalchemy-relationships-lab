"""Create tables with relationships

Revision ID: 3599de996267
Revises: 
Create Date: 2025-06-20 00:39:21.845259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3599de996267'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bio_text', sa.Text(), nullable=False),
    sa.Column('speaker_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('speakers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session_speakers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('speaker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name=op.f('fk_session_speakers_session_id_sessions')),
    sa.ForeignKeyConstraint(['speaker_id'], ['speakers.id'], name=op.f('fk_session_speakers_speaker_id_speakers')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_speakers')
    op.drop_table('speakers')
    op.drop_table('sessions')
    op.drop_table('events')
    op.drop_table('bios')
    # ### end Alembic commands ###
