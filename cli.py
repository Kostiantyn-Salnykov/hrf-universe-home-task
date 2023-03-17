import sqlalchemy.exc
import typer

from home_task.db import engine

app = typer.Typer(name="super CLI")


@app.command(name="update")
def update():
    # TODO: Update materialized view parameter
    with engine.connect() as connection:
        try:
            connection.execute(statement="REFRESH MATERIALIZED VIEW CONCURRENTLY days_to_hire_statistics;")
        except sqlalchemy.exc.NotSupportedError:
            connection.execute(statement="REFRESH MATERIALIZED VIEW days_to_hire_statistics;")


if __name__ == "__main__":
    app()
