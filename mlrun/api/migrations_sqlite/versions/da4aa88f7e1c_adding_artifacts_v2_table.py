# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""adding artifacts_v2 table

Revision ID: da4aa88f7e1c
Revises: 4acd9430b093
Create Date: 2023-06-27 17:55:19.401051

"""
import sqlalchemy as sa
from alembic import op

from mlrun.api.utils.db.sql_collation import SQLCollationUtil

# revision identifiers, used by Alembic.
revision = "da4aa88f7e1c"
down_revision = "4acd9430b093"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "artifacts_v2",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.String(length=255), nullable=True),
        sa.Column("project", sa.String(length=255), nullable=True),
        sa.Column("key", sa.String(length=255), nullable=True),
        sa.Column("kind", sa.String(length=255), nullable=True, index=True),
        sa.Column("producer_id", sa.String(length=255), nullable=True),
        sa.Column("iteration", sa.Integer(), nullable=True),
        sa.Column("best_iteration", sa.BOOLEAN(), nullable=True, index=True),
        sa.Column("object", sa.BLOB(), nullable=True),
        sa.Column("created", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uid", "project", "key", name="_artifacts_v2_uc"),
    )
    op.create_table(
        "artifacts_v2_labels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "name",
            sa.String(255, collation=SQLCollationUtil.collation()),
            nullable=True,
        ),
        sa.Column(
            "value",
            sa.String(255, collation=SQLCollationUtil.collation()),
            nullable=True,
        ),
        sa.Column("parent", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent"],
            ["artifacts_v2.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "parent", name="_artifacts_v2_labels_uc"),
    )
    op.create_table(
        "artifacts_v2_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "project",
            sa.String(255, collation=SQLCollationUtil.collation()),
            nullable=True,
        ),
        sa.Column(
            "name",
            sa.String(255, collation=SQLCollationUtil.collation()),
            nullable=True,
        ),
        sa.Column("obj_id", sa.Integer(), nullable=True),
        sa.Column(
            "obj_name",
            sa.String(255, collation=SQLCollationUtil.collation()),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["obj_id"],
            ["artifacts_v2.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project", "name", "obj_name", name="_artifacts_v2_tags_uc"
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("artifacts_v2")
    op.drop_table("artifacts_v2_labels")
    op.drop_table("artifacts_v2_tags")
    # ### end Alembic commands ###
