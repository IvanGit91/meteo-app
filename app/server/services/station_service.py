from app.server import db
from app.server.models.station import Station


class StationService:
    @staticmethod
    def create_station(code, city, latitude, longitude, installed_at):
        station = Station(
            code=code,
            city=city,
            latitude=latitude,
            longitude=longitude,
            installed_at=installed_at
        )
        db.session.add(station)
        db.session.commit()
        return station

    @staticmethod
    def get_stations(page):
        return db.paginate(Station.query, page=page, per_page=10, error_out=False).items

    @staticmethod
    def get_station_by_id(id):
        return Station.query.filter_by(id=id).first()

    @staticmethod
    def get_station_by_code(code):
        return Station.query.filter_by(code=code).first()

    @staticmethod
    def delete_station(code):
        station = StationService.get_station_by_code(code)
        if station:
            db.session.delete(station)
            db.session.commit()
