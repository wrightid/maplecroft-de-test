from flask import url_for

from api.extensions import pwd_context
from api.models import User


def test_get_all_sites(client, db, site_factory, admin_headers):
    """test_get_all_sites

    Get all sites and test works without a parameter

    :param client:
    :param db:
    :param site_factory:
    :param admin_headers:
    """
    sites_url = url_for('api.sites')
    sites = site_factory.create_batch(30)

    db.session.add_all(sites)
    db.session.commit()

    rep = client.get(sites_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()

    assert results["total"] == 30

    for site in sites:
        assert any(s["id"] == site.id for s in results["results"])

def test_get_all_sites_with_filter(client, db, site_factory, area_factory, area_site_factory, admin_headers):
    """test_get_all_sites_with_filter

    Test that the filter works

    Params defined in conftest.py

    :param client:
    :param db:
    :param site_factory:
    :param area_factory:
    :param area_site_factory:
    :param admin_headers:
    """
    area_filter = 'area2'
    sites_url = url_for('api.sites', admin_area=area_filter)
    sites = site_factory.create_batch(30)
    areas = area_factory.create_batch(30)
    areasites = area_site_factory.create_batch(30)
    db.session.add_all(sites)
    db.session.add_all(areas)
    db.session.add_all(areasites)
    db.session.commit()

    rep = client.get(sites_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()

    assert results["total"] == 6

    for site in areasites:
        if site.area_id == area_filter:
            assert any(s["id"] == site.site_id for s in results["results"])
        else:
            assert not any(s["id"] == site.site_id for s in results["results"])
