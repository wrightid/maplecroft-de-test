from flask import url_for

from api.extensions import pwd_context
from api.models import Site, AreaSite, Area


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

def test_get_all_sites_with_filter(client, db, site_factory, area_factory, admin_headers):
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
    db.session.add_all(sites)
    db.session.add_all(areas)
    db.session.commit()

    area = db.session.query(Area).get(area_filter)

    count = 0
    linked_count = 0
    area_sites = []
    for site in db.session.query(Site).all():
        if count % 5:
            area_site = AreaSite()
            area_site.site_id = site.id
            area_site.area_id = area.id
            db.session.add(area_site)
            db.session.commit()
            linked_count = linked_count + 1
            area_sites.append(area_site)
        count = count + 1

    rep = client.get(sites_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()

    assert results["total"] == linked_count

    for site in area_sites:
        if site.area_id == area_filter:
            assert any(s["id"] == site.site_id for s in results["results"])
        else:
            assert not any(s["id"] == site.site_id for s in results["results"])
