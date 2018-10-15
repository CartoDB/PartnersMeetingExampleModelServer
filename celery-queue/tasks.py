import os
import sys
import time
from celery import Celery
from sklearn.datasets import make_gaussian_quantiles
import numpy as np
import pandas as pd
from cartoframes import CartoContext, Credentials
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

target_scaler = joblib.load('model/target_scaler.save')
features_scaler= joblib.load('model/feature_scaler.save')
full_model = joblib.load( 'model/model.save')
augmented_data_min_max_scaler = joblib.load( 'model/do_scaler.save')


@celery.task(name='tasks.predict')
def predict(username,api_key, input_table, output_table):
    creds = Credentials(username=username, key=api_key)
    cc = CartoContext(creds=creds)
    data_obs_measures = [{'numer_id': 'us.census.acs.B25058001'},
			 {'numer_id': 'us.census.acs.B25071001'},
			 {'numer_id': 'us.census.acs.B25081002'},
			 ]
    locations = cc.data(input_table, data_obs_measures)

    features = locations[['minimum_nights', 'review_scores_accuracy', 'review_scores_location']]
    do_features = locations[['mortgaged_housing_units_2011_2015_by_owner_occupied_housing_uni', 'percent_income_spent_on_rent_2011_2015','median_rent_2011_2015']].fillna(0)

    normed_do = pd.DataFrame(augmented_data_min_max_scaler.transform(do_features), columns=do_features.columns)
    normed_features = pd.DataFrame(features_scaler.transform(features), columns=features.columns)


    do_and_bnb_features =  pd.merge(normed_features,normed_do, left_index=True, right_index=True)
    logger.info('Have data, running model')

    result = full_model.predict(do_and_bnb_features)
    logger.info('model run')

    denormed_results = target_scaler.inverse_transform(np.exp(result.reshape(-1,1)))
    logger.info('have results')
    locations = locations.assign(prediciton = denormed_results)
    logger.info('writing back to ', )
    cc.write(locations,output_table, overwrite=True, privacy='public')
    logger.info('all done')
    return "https://team.carto.com/u/{}/dataset/{}".format(username,output_table)


