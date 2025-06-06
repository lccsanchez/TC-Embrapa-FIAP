"""estrutura inicial

Revision ID: c1d387864fdc
Revises:
Create Date: 2025-05-22 18:20:59.368616

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1d387864fdc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "importacao_exportacao",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("pais", sa.String(length=200), nullable=False),
        sa.Column("classificacao", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "produtos",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("control", sa.String(length=100), nullable=True),
        sa.Column("produto", sa.String(length=200), nullable=True),
        sa.Column("categoria", sa.String(length=100), nullable=True),
        sa.Column("classificacao", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("username", sa.String(length=100), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("hashed_password", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=True),
        sa.Column("phone_number", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "registros",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("id_produto", sa.String(length=50), nullable=False),
        sa.Column("tipo_operacao", sa.String(length=20), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=20, scale=0), nullable=False),
        sa.ForeignKeyConstraint(["id_produto"], ["produtos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "registros_importacao_exportacao",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("id_pais", sa.String(length=50), nullable=False),
        sa.Column("tipo_operacao", sa.String(length=20), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=20, scale=0), nullable=False),
        sa.Column("valor", sa.Numeric(precision=20, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_pais"], ["importacao_exportacao.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("registros_importacao_exportacao")
    op.drop_table("registros")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("produtos")
    op.drop_table("importacao_exportacao")
    # ### end Alembic commands ###
