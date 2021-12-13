import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from api.extensions import db
    from api.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@mail.com",
                password="admin", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


@cli.command("load_sites")
@click.option('--adm3', is_flag=True, help="ADM3 only")
@with_appcontext
def load_sites(adm3):
    """
    We need to pull all sites from the bikes api

    http://api.citybik.es/v2/networks

    Determine what admin area they are in by using the GeoBoundaries dataset

    For example the admin areas for Great Britain are...

    https://www.geoboundaries.org/gbRequest.html?ISO=GBR&ADM=ADM3

    And then populate the database so that we can query by admin area

    :return:
    """
    from api.data_import import DataImport

    importer = DataImport()

    try:
        importer.load_data()
    except Exception as e:
        # Just print the response if the connection fail
        print("Unable to get data")
        print(e)
        return

    levels = []
    if adm3:
        levels.append("ADM3")
    importer.import_all_data(levels)


if __name__ == "__main__":
    cli()
