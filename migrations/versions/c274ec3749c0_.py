"""empty message

Revision ID: c274ec3749c0
Revises: 
Create Date: 2021-04-19 16:49:19.636775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c274ec3749c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_at_ip', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    # change id field to BigInt for psql on heroku
    # psql doesn't suppoer unsigned
    sa.Column('handle', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=False),
    sa.Column('background_image', sa.String(length=20), nullable=False),
    sa.Column('bio', sa.String(length=160), nullable=False),
    sa.Column('location', sa.String(length=30), nullable=False),
    sa.Column('website', sa.String(length=100), nullable=False),
    sa.Column('last_read_message_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('handle'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('follower',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('following_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['user.id'], )
    )
    op.create_table('message',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=500), nullable=False),
    sa.Column('read_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('op_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['op_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('liker',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('liker')
    op.drop_table('post')
    op.drop_table('message')
    op.drop_table('follower')
    op.drop_table('user')
    # ### end Alembic commands ###
