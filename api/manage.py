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
@with_appcontext
def load_sites():
    """
    We need to pull all sites from the bikes api

    http://api.citybik.es/v2/networks

    Determine what admin area they are in by using the GeoBoundaries dataset

    For example the admin areas for Great Britain are...

    https://www.geoboundaries.org/gbRequest.html?ISO=GBR&ADM=ADM3

    And then populate the database so that we can query by admin area

    :return:
    """
    from api.extensions import db
    from api.models.site import Site
    from api.remote import get_networks

    try:
        networks = get_networks
    except Exception as e:
        # Just print the response if the connection fail
        print("Unable to get site data")
        print(e)
        return

    # Assume we'll just replace any existing data
    # We know that we've got data because of no exception above
    # No TRUNCATE in SQLlite
    # db.engine.execute("TRUNCATE TABLE site;")
    db.engine.execute("DELETE FROM site;")

    i = 0
    for network in networks():
        site = Site()
        site.id = network["id"]
        site.name = network["name"]
        site.latitude = network["location"]["latitude"]
        site.longitude = network["location"]["longitude"]
        site.country = network["location"]["country"]
        db.session.add(site)
        i += 1
        # Commit every 50
        # Not really necessary with such a small result set
        if i % 50 == 0:
            db.session.commit()
    db.session.commit()
    print(f'{i} sites loaded')


if __name__ == "__main__":
    cli()
