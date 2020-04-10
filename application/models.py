from . import db


class RawData(db.Model):
    """Model for user accounts."""

    __tablename__ = 'raw_data'
    id = db.Column(db.Integer, primary_key=True)
    age_bracket = db.Column(db.String(64), index=False, unique=False, nullable=True)
    backup_notes = db.Column(db.String(164), index=False, unique=False, nullable=True)
    contracted_from = db.Column(db.String(164), index=False, unique=False, nullable=True)
    current_status = db.Column(db.String(64), index=False, unique=False, nullable=True)
    date_announced = db.Column(db.Date, index=False, unique=False, nullable=True)
    detected_city = db.Column(db.String(64), index=False, unique=False, nullable=True)
    detected_district = db.Column(db.String(64), index=False, unique=False, nullable=True)
    detected_state = db.Column(db.String(64), index=False, unique=False, nullable=True)
    estimated_on_set_date = db.Column(db.String(32), index=False, unique=False, nullable=True)
    gender = db.Column(db.String(14), index=False, unique=False, nullable=True)
    nationality = db.Column(db.String(324), index=False, unique=False, nullable=True)
    notes = db.Column(db.String(164), index=False, unique=False, nullable=True)
    patient_number = db.Column(db.Integer, index=True, unique=True, nullable=False)
    source1 = db.Column(db.String(164), index=False, unique=False, nullable=True)
    source2 = db.Column(db.String(164), index=False, unique=False, nullable=True)
    source3 = db.Column(db.String(164), index=False, unique=False, nullable=True)
    state_code = db.Column(db.String(14), index=False, unique=False, nullable=True)
    state_patient_number = db.Column(db.String(16), index=False, unique=False, nullable=True)
    status_change_date = db.Column(db.Date, index=False, unique=False, nullable=True)
    type_of_transmission = db.Column(db.String(14), index=False, unique=False, nullable=True)

    def __repr__(self) -> str:
        return super().__repr__()


class StateDailyData(db.Model):
    """Model for daily state increments."""

    __tablename__ = 'daily_state_data'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(32), index=False, unique=False, nullable=True)
    state_code = db.Column(db.String(4), index=False, unique=False, nullable=True)
    count = db.Column(db.Integer, index=False, unique=False, nullable=True)
    status = db.Column(db.String(32), index=False, unique=False, nullable=True)
    capture_date = db.Column(db.Date, index=False, unique=False, nullable=True)

    def __repr__(self) -> str:
        return super().__repr__()
