from typing import Dict, List, Generator
from decimal import Decimal

import requests
import logging

import geopandas
from shapely.geometry import Point

from api.extensions import db
from api.models import Site
from api.models import Area
from api.models import AreaSite


class DataImport(object):

    def __init__(self) -> None:

        self.networks_api = "http://api.citybik.es/v2/networks"
        self.boundaries_api = "https://www.geoboundaries.org/gbRequest.html"

        self.boundaries = None
        self.networks = None

        self.logger = logging.getLogger(__name__)
    
    def load_data(self):
        """load_data - make initial API calls and make sure they work"""
        try:
            r = requests.get(self.networks_api)
            self.networks = r.json()["networks"]

        except Exception as e:
            # Just print the response if the connection fail
            self.logger.error("Unable to get site data", exc_info=1)
            raise e

        try:
            r = requests.get(self.boundaries_api)
            self.boundaries = r.json()

        except Exception as e:
            # Just print the response if the connection fail
            self.logger.error("Unable to get boundary data", exc_info=1)
            raise e

    def get_networks(self):
        """get_networks - a generator to return the sites from the downloaded
        data"""
        #
        for network in self.networks:
            yield network

    def get_geo_boundaries(self, levels: List[str]) -> Generator[Dict, None, None]:
        """get_geo_boundaries

        :param levels: filter to include only these levels e.g. ADM3
        :type levels: List[str]
        """
        # Uses the legacy API

        for boundary in self.boundaries:
            if levels and boundary["boundaryType"] not in levels:
                continue
            dlPath = boundary["gjDownloadURL"]
            geo_boundary = requests.get(dlPath).json()

            yield geo_boundary

    def get_features(self, geo_boundary: Dict) -> Generator[Dict, None, None]:
        """get_features - a generator to return all the features i.e. areas
        with the FeatureCollection

        :param geo_boundary:
        """
        for area in geo_boundary["features"]:
            yield area

    def sites_to_geo_data_frame(self, sites: List[Site]) -> geopandas.GeoDataFrame:
        """sites_to_geo_data_frame - create a GeoDataFrame containing all the
        sites in the list

        :param sites: a list of site using internal rep
        :type sites: List[Site]
        :rtype: geopandas.GeoDataFrame
        """
        site_names = []
        site_coords = []
        for site in sites:
            site_names.append(site.id)
            y = Decimal(site.latitude)
            x = Decimal(site.longitude)
            site_coords.append(Point(x, y))

        sites = geopandas.GeoDataFrame({
            "name": site_names,
            "geometry": site_coords
        })

        return sites

    def load_sites_to_db(self):
        # Assume we'll just replace any existing data
        # We know that we've got data because of no exception above
        # No TRUNCATE in SQLlite
        # db.engine.execute("TRUNCATE TABLE site;")
        db.engine.execute("DELETE FROM site;")

        i = 0

        sites = []

        for network in self.get_networks():
            site = Site()
            site.id = network["id"]
            site.name = network["name"]
            site.latitude = network["location"]["latitude"]
            site.longitude = network["location"]["longitude"]
            site.country = network["location"]["country"]
            db.session.add(site)
            sites.append(site)
            i += 1
            # Commit every 50
            # Not really necessary with such a small result set
            if i % 50 == 0:
                db.session.commit()
        db.session.commit()

        print(f'{i} sites loaded')

        return sites

    def insert_feature(self, feature):
        """insert_feature - inserts a feature (area) into the database

        :param feature:
        """

        area = Area()
        area.id = feature["properties"]["shapeID"]
        area.shape_group = feature["properties"]["shapeGroup"]
        area.shape_name = feature["properties"]["shapeName"]
        area.shape_type = feature["properties"]["shapeType"]

        # Could store whole feature or feature["geometry"] if useful

        db.session.add(area)

    def import_all_data(self, levels: List[str]):
        """import_all_data as previously fetched using load_data into the
        database

        :param levels:
        :type levels: List[str]
        """

        sites = self.load_sites_to_db()

        geo_sites = self.sites_to_geo_data_frame(sites)

        self.load_and_link_areas(geo_sites, levels)

    def insert_point_area(self, point_id, shape_id):
        """insert_point_area - create a new relationship between a site and an
        area

        :param point_id:
        :param shape_id:
        """

        relationship = AreaSite()
        relationship.area_id = shape_id
        relationship.site_id = point_id

        db.session.add(relationship)

    def load_and_link_areas(self, sites: geopandas.GeoDataFrame, levels: List[str]):
        """load_and_link_areas
                Clear out existing data and sites with the previously loaded
                geo data

        :param sites:
        :type sites: geopandas
        :param GeoDataFrame:
        :param levels:
        :type levels: List[str]
        """
        db.engine.execute("DELETE FROM area_site;")
        db.engine.execute("DELETE FROM area;")
        j = 0
        for area in self.get_geo_boundaries(levels):

            # Load all the features, we want them even if no sites presents
            for feature in self.get_features(area):
                self.insert_feature(feature)
            db.session.commit()

            results = self.get_sites_in_area(sites, area)

            self.logger.info("%d in %s", len(results), area)

            results.apply(lambda row: self.insert_point_area(row['name'], row['shapeID']), axis=1)

            db.session.commit()

            j += 1

        print(f'{j} boundaries loaded')

    def get_sites_in_area(self, sites: geopandas.GeoDataFrame, area: Dict) -> geopandas.GeoDataFrame:
        """get_sites_in_area - get all the sites in an area

        :param sites:
        :param area:
        """
        df = geopandas.GeoDataFrame.from_features(area)

        results = geopandas.sjoin(sites, df)

        return results
