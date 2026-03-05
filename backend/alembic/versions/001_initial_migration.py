"""initial migration

Revision ID: 001
Revises:
Create Date: 2026-03-05

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 accounts 表
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.String(length=100), nullable=False, comment='昵称'),
        sa.Column('cookies', sa.Text(), nullable=False, comment='Cookies (加密存储)'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='账号状态'),
        sa.Column('last_login', sa.DateTime(), nullable=True, comment='最后登录时间'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)

    # 创建 products 表
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False, comment='商品标题'),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False, comment='价格'),
        sa.Column('description', sa.Text(), nullable=True, comment='商品描述'),
        sa.Column('images', sa.Text(), nullable=True, comment='图片列表 (JSON数组)'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='商品状态'),
        sa.Column('xianyu_id', sa.String(length=100), nullable=True, comment='闲鱼商品ID'),
        sa.Column('account_id', sa.Integer(), nullable=True, comment='所属账号ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

    # 创建 card_keys 表
    op.create_table(
        'card_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.Text(), nullable=False, comment='卡密内容'),
        sa.Column('product_id', sa.Integer(), nullable=False, comment='所属商品ID'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='卡密状态'),
        sa.Column('used_at', sa.DateTime(), nullable=True, comment='使用时间'),
        sa.Column('used_order_id', sa.Integer(), nullable=True, comment='使用的订单ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_keys_id'), 'card_keys', ['id'], unique=False)

    # 创建 orders 表
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False, comment='账号ID'),
        sa.Column('product_id', sa.Integer(), nullable=False, comment='商品ID'),
        sa.Column('xianyu_order_id', sa.String(length=100), nullable=True, comment='闲鱼订单ID'),
        sa.Column('buyer_nickname', sa.String(length=100), nullable=False, comment='买家昵称'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='订单状态'),
        sa.Column('card_key_id', sa.Integer(), nullable=True, comment='卡密ID'),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False, comment='订单金额'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('paid_at', sa.DateTime(), nullable=True, comment='支付时间'),
        sa.Column('shipped_at', sa.DateTime(), nullable=True, comment='发货时间'),
        sa.Column('completed_at', sa.DateTime(), nullable=True, comment='完成时间'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['card_key_id'], ['card_keys.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)

    # 创建 messages 表
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False, comment='账号ID'),
        sa.Column('xianyu_message_id', sa.String(length=100), nullable=True, comment='闲鱼消息ID'),
        sa.Column('from_user', sa.String(length=100), nullable=False, comment='发送者'),
        sa.Column('to_user', sa.String(length=100), nullable=False, comment='接收者'),
        sa.Column('content', sa.Text(), nullable=False, comment='消息内容'),
        sa.Column('is_read', sa.Boolean(), nullable=True, comment='是否已读'),
        sa.Column('reply_content', sa.Text(), nullable=True, comment='回复内容'),
        sa.Column('is_auto_reply', sa.Boolean(), nullable=True, comment='是否自动回复'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)

    # 创建 alerts 表
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False, comment='告警类型'),
        sa.Column('content', sa.Text(), nullable=False, comment='告警内容'),
        sa.Column('account_id', sa.Integer(), nullable=True, comment='关联账号ID'),
        sa.Column('is_resolved', sa.Boolean(), nullable=True, comment='是否已解决'),
        sa.Column('resolved_at', sa.DateTime(), nullable=True, comment='解决时间'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_id'), 'alerts', ['id'], unique=False)

    # 创建 settings 表
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=100), nullable=False, comment='配置键'),
        sa.Column('value', sa.Text(), nullable=True, comment='配置值'),
        sa.Column('description', sa.String(length=255), nullable=True, comment='配置描述'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_settings_id'), 'settings', ['id'], unique=False)
    op.create_index(op.f('ix_settings_key'), 'settings', ['key'], unique=True)

    # 创建 blacklist 表
    op.create_table(
        'blacklist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.String(length=100), nullable=False, comment='用户昵称'),
        sa.Column('reason', sa.Text(), nullable=True, comment='拉黑原因'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blacklist_id'), 'blacklist', ['id'], unique=False)
    op.create_index(op.f('ix_blacklist_nickname'), 'blacklist', ['nickname'], unique=True)

    # 创建 logs 表
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('level', sa.String(length=20), nullable=False, comment='日志级别'),
        sa.Column('category', sa.String(length=50), nullable=False, comment='日志分类'),
        sa.Column('content', sa.Text(), nullable=False, comment='日志内容'),
        sa.Column('account_id', sa.Integer(), nullable=True, comment='关联账号ID'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logs_id'), 'logs', ['id'], unique=False)
    op.create_index(op.f('ix_logs_created_at'), 'logs', ['created_at'], unique=False)


def downgrade() -> None:
    # 删除所有表（按依赖顺序）
    op.drop_index(op.f('ix_logs_created_at'), table_name='logs')
    op.drop_index(op.f('ix_logs_id'), table_name='logs')
    op.drop_table('logs')

    op.drop_index(op.f('ix_blacklist_nickname'), table_name='blacklist')
    op.drop_index(op.f('ix_blacklist_id'), table_name='blacklist')
    op.drop_table('blacklist')

    op.drop_index(op.f('ix_settings_key'), table_name='settings')
    op.drop_index(op.f('ix_settings_id'), table_name='settings')
    op.drop_table('settings')

    op.drop_index(op.f('ix_alerts_id'), table_name='alerts')
    op.drop_table('alerts')

    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')

    op.drop_index(op.f('ix_card_keys_id'), table_name='card_keys')
    op.drop_table('card_keys')

    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')

    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_table('accounts')
