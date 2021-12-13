import pytest

import json

import geopandas
from shapely.geometry import Point

from decimal import Decimal

from api.data_import import DataImport
from api.models import Site


def test_data_import_bad_endpoint():
    """test_data_import_bad_endpoint
    Make sure that an exception is raised if there is a problem with the
    endpoint

    """

    importer = DataImport()
    importer.networks_api = "http://this.is.not.a.url/"

    with pytest.raises(Exception):
        importer.load_data()


def test_data_import_lookup():
    """test_data_import_lookup

    Check that the lookup of sites within areas is working correctly
    In particular check that lat and lng are the right way round

    """

    importer = DataImport()

    importer.boundaries = [
        {
            "boundaryID": "GBR-ADM3-3_0_0-G615",
            "boundaryISO": "GBR",
            "boundaryYear": "2018.0",
            "boundaryType": "ADM3",
            "boundarySource-1": "Office for National Statistics Open Geography Portal",
            "boundarySource-2": "",
            "boundaryLicense": "Open Data Commons Open Database License 1.0",
            "licenseDetail": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "licenseSource": "https://geoportal.statistics.gov.uk/datasets/wards-december-2018-full-extent-boundaries-uk?geometry=-96.518%2C48.053%2C70.738%2C64.739",
            "boundarySourceURL": "https://geoportal.statistics.gov.uk/datasets/wards-december-2018-full-extent-boundaries-uk?geometry=-96.518%2C48.053%2C70.738%2C64.739",
            "boundaryUpdate": "2020-05-25",
            "downloadURL": "https://geoboundaries.org/data/geoBoundaries-3_0_0/GBR/ADM3/geoBoundaries-3_0_0-GBR-ADM3-all.zip",
            "gjDownloadURL": "https://geoboundaries.org/data/geoBoundaries-3_0_0/GBR/ADM3/geoBoundaries-3_0_0-GBR-ADM3.geojson",
            "imagePreview": "https://geoboundaries.org/data/geoBoundaries-3_0_0/GBR/ADM3/geoBoundariesPreview-3_0_0-GBR-ADM3.png",
        },
    ]

    sites = []

    site = Site()
    site.id = "London"
    site.name = "London"
    site.latitude = "51.5"
    site.longitude = "0.0"
    sites.append(site)

    site1 = Site()
    site1.id = "Valencia"
    site1.name = "Valencia"
    site1.latitude = "39.28"
    site1.longitude = "0.23"
    sites.append(site1)

    # Swap coords around so make sure that we're looking the right thing up
    site2 = Site()
    site2.id = "madeup"
    site2.name = "madeup"
    site2.latitude = "0.0"
    site2.longitude = "51.5"
    sites.append(site2)

    geo_sites = importer.sites_to_geo_data_frame(sites)

    for boundary in importer.get_geo_boundaries(["ADM3"]):
        results = importer.get_sites_in_area(geo_sites, boundary)

    assert len(results) == 1
    assert results.iloc[0]["name"] == "London"
