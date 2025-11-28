"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create companies table
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cnpj', sa.String(14), nullable=False),
        sa.Column('razao_social', sa.String(255), nullable=True),
        sa.Column('cnae', sa.String(7), nullable=True),
        sa.Column('municipio', sa.String(100), nullable=True),
        sa.Column('uf', sa.String(2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_companies_cnpj', 'companies', ['cnpj'])
    op.create_index('ix_companies_cnae', 'companies', ['cnae'])
    op.create_index('ix_companies_municipio', 'companies', ['municipio'])

    # Create convencoes table
    op.create_table(
        'convencoes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('instrumento_id', sa.String(50), nullable=False, unique=True),
        sa.Column('titulo', sa.String(500), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=True),
        sa.Column('data_publicacao', sa.Date(), nullable=True),
        sa.Column('data_vigencia_inicio', sa.Date(), nullable=True),
        sa.Column('data_vigencia_fim', sa.Date(), nullable=True),
        sa.Column('sindicato_empregador', sa.String(255), nullable=True),
        sa.Column('sindicato_trabalhador', sa.String(255), nullable=True),
        sa.Column('municipio', sa.String(100), nullable=True),
        sa.Column('uf', sa.String(2), nullable=True),
        sa.Column('cnae', sa.String(7), nullable=True),
        sa.Column('documento_url', sa.Text(), nullable=True),
        sa.Column('documento_path', sa.Text(), nullable=True),
        sa.Column('texto_extraido', sa.Text(), nullable=True),
        sa.Column('formato_documento', sa.String(20), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='PROCESSANDO'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('ix_convencoes_instrumento_id', 'convencoes', ['instrumento_id'])
    op.create_index('ix_convencoes_data_publicacao', 'convencoes', ['data_publicacao'])
    op.create_index('ix_convencoes_cnae', 'convencoes', ['cnae'])
    op.create_index('ix_convencoes_municipio', 'convencoes', ['municipio'])

    # Create convencoes_empresas table
    op.create_table(
        'convencoes_empresas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('convencao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('relevancia_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['convencao_id'], ['convencoes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    )

    # Create convencoes_metadados table
    op.create_table(
        'convencoes_metadados',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('convencao_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chave', sa.String(100), nullable=False),
        sa.Column('valor', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['convencao_id'], ['convencoes.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_convencoes_metadados_chave', 'convencoes_metadados', ['chave'])

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('convencao_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=True),
        sa.Column('titulo', sa.String(255), nullable=True),
        sa.Column('mensagem', sa.Text(), nullable=True),
        sa.Column('lida', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['convencao_id'], ['convencoes.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_notifications_created_at', 'notifications', ['created_at'])

    # Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('email_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('push_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('frequencia', sa.String(20), nullable=False, server_default='IMEDIATO'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('notification_preferences')
    op.drop_table('notifications')
    op.drop_table('convencoes_metadados')
    op.drop_table('convencoes_empresas')
    op.drop_table('convencoes')
    op.drop_table('companies')
    op.drop_table('users')

