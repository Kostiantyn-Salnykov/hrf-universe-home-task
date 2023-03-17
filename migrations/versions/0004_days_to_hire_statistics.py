"""days_to_hire_statistics

Revision ID: 0004
Revises: 991ecb2bf269
Create Date: 2023-03-17 15:27:17.114798+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "991ecb2bf269"
branch_labels = None
depends_on = None

VIEW_NAME = "days_to_hire_statistics"


def upgrade() -> None:
    op.execute(
        sqltext=f"""
        CREATE MATERIALIZED VIEW public.{VIEW_NAME}
        AS
        SELECT standard_job_id,
            country_code,
            AVG(DAYS_TO_HIRE) as avg,
            percentile_cont(0.10) WITHIN GROUP (order by days_to_hire) as min,
            percentile_cont(0.90) within group (order by days_to_hire) as max,
            COUNT(*) as number_of_job_posts
        FROM job_posting
        WHERE days_to_hire IS NOT NULL
            AND days_to_hire > 1
        GROUP BY standard_job_id,
            country_code
        HAVING COUNT(*) > 5
        WITH NO DATA;
        """
    )
    op.create_index(
        index_name="ix_standard_job_id",
        table_name=VIEW_NAME,
        columns=("standard_job_id", "country_code"),
        schema="public",
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(index_name="ix_standard_job_id")
    op.execute(sqltext=f"DROP MATERIALIZED VIEW IF EXISTS public.{VIEW_NAME};")
