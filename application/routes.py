from flask import request, render_template, make_response
from flask import current_app as app
from .models import StateDailyData
from .util import *
import atexit
import requests
import json
import logging
from . import crontab


@app.route('/save_raw_data', methods=['GET'])
def fetch_raw_data():
    """Used to fetch raw data from covid-19 API."""

    raw_data_response = requests.get('https://api.covid19india.org/raw_data.json')
    raw_data_response = json.loads(raw_data_response.text)

    try:
        for data in raw_data_response['raw_data']:

            date_announce, estimated_set, status_change = validate_dates(data['dateannounced'],
                                                                         data['estimatedonsetdate'],
                                                                         data['statuschangedate'])
            patient = RawData(age_bracket=data['agebracket'],
                              backup_notes=data['backupnotes'],
                              contracted_from=data['contractedfromwhichpatientsuspected'],
                              current_status=data['currentstatus'],
                              date_announced=date_announce,
                              detected_city=data['detectedcity'], detected_district=data['detecteddistrict'],
                              detected_state=data['detectedstate'],
                              estimated_on_set_date=estimated_set,
                              gender=data['gender'], nationality=data['nationality'],
                              notes=data['notes'], patient_number=int(data['patientnumber']),
                              source1=data['source1'], source2=data['source2'], source3=data['source1'],
                              state_code=data['statecode'], state_patient_number=data['statepatientnumber'],
                              status_change_date=status_change, type_of_transmission=data['typeoftransmission'])

            db.session.add(patient)
            db.session.commit()
            print(str(patient.patient_number)+'added successfully.')
        return 'All added to DB successfully!'
    except Exception as ex:
        print(ex)
        return ex


@crontab.job(minute='1')
# @app.route('/update_patient_data', methods=['GET'])
def update_patient_data():
    logging.info('Starting job for updating patients data')
    raw_data_response = requests.get('https://api.covid19india.org/raw_data.json')
    raw_data_response = json.loads(raw_data_response.text)
    max_patient_number = db.session.query(db.func.max(RawData.patient_number)).scalar()

    try:
        for data in raw_data_response['raw_data']:
            if int(data['patientnumber']) > max_patient_number:

                date_announce, estimated_set, status_change = validate_dates(data['dateannounced'],
                                                                             data['estimatedonsetdate'],
                                                                             data['statuschangedate'])
                patient = RawData(age_bracket=data['agebracket'],
                                  backup_notes=data['backupnotes'],
                                  contracted_from=data['contractedfromwhichpatientsuspected'],
                                  current_status=data['currentstatus'],
                                  date_announced=date_announce,
                                  detected_city=data['detectedcity'], detected_district=data['detecteddistrict'],
                                  detected_state=data['detectedstate'],
                                  estimated_on_set_date=estimated_set,
                                  gender=data['gender'], nationality=data['nationality'],
                                  notes=data['notes'], patient_number=int(data['patientnumber']),
                                  source1=data['source1'], source2=data['source2'], source3=data['source1'],
                                  state_code=data['statecode'], state_patient_number=data['statepatientnumber'],
                                  status_change_date=status_change, type_of_transmission=data['typeoftransmission'])

                db.session.add(patient)
                db.session.commit()
                print(str(patient.patient_number)+'added successfully.')
        return 'Patients DB updated successfully!'
    except Exception as ex:
        print(ex)
        return ex


@app.route('/save_states_daily', methods=['GET'])
def save_states_daily_data():
    """Used to fetch raw data from covid-19 API."""

    raw_data_response = requests.get('https://api.covid19india.org/states_daily.json')
    raw_data_response = json.loads(raw_data_response.text)
    try:
        for data in raw_data_response['states_daily']:
            state_date = validate_state_daily_date(data['date'])
            status = data['status']
            for state_code in data:
                if state_code != 'date' and state_code != 'status':
                    if len(data[state_code]) > 0:
                        case_count = data[state_code]
                    else:
                        case_count = 0
                    state_daily_data = StateDailyData(state_code=state_code, state=get_state_by_state_code(state_code),
                                                      count=case_count, status=status, capture_date=state_date)
                    db.session.add(state_daily_data)
                    db.session.commit()
                    print(str(state_daily_data.state)+' added successfully for date: '+data['date'])
        return 'All added to DB successfully!'
    except Exception as ex:
        print(ex)
        return ex


@crontab.job(minute=5)
# @app.route('/update_states_daily', methods=['GET'])
def update_states_daily_data():
    """Used to fetch raw data from covid-19 API."""
    logging.info('Starting job for updating daily states data')
    raw_data_response = requests.get('https://api.covid19india.org/states_daily.json')
    raw_data_response = json.loads(raw_data_response.text)
    try:
        max_date = db.session.query(db.func.max(StateDailyData.capture_date)).scalar()
        for data in raw_data_response['states_daily']:
            state_date = validate_state_daily_date(data['date'])
            if state_date > max_date:
                status = data['status']
                for state_code in data:
                    if state_code != 'date' and state_code != 'status':
                        if len(data[state_code]) > 0:
                            case_count = data[state_code]
                        else:
                            case_count = 0
                        state_daily_data = StateDailyData(state_code=state_code, state=get_state_by_state_code(state_code),
                                                          count=case_count, status=status, capture_date=state_date)
                        db.session.add(state_daily_data)
                        db.session.commit()
                        print(str(state_daily_data.state)+' added successfully for date: '+data['date'])
        return 'All added to DB successfully!'
    except Exception as ex:
        print(ex)
        return ex


@app.route('/state_pattern/<code>', methods=['GET'])
def state_pattern(code):
    result = {
        'count': [],
        'date': []
    }

    query = StateDailyData.query.filter_by(state_code='hr')
    results = query.all()
    for data in results:
        result['count'].append(data.count)
        result['date'].append(data.capture_date.strftime("%d/%m/%Y"))
    return json.dumps(result)


# atexit.register(lambda: crontab.shutdown(wait=False))
