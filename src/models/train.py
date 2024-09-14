import pandas as pd
import numpy as np

import argparse

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost

import mlflow


def parse_arg():
    parser = argparse.ArgumentParser(description='House Prices ML Predictor')
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.3,
        help="""
    In machine learning and statistics, the learning rate is a tuning parameter /n
    in an optimization algorithm that determines the step size at each iteration /n
    while moving toward a minimum of a loss function.
    """
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=5,
        help="This parameter controls the maximum depth of the tree."
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=0,
        help="""
    Seeds are essentially random numbers or vectors that are used to 
    initialize various processes, ensuring that the results are not 
    deterministic and exhibit desirable properties
    """
    )
    return parser.parse_args()



df = pd.read_csv('data/external/casas.csv')

X = df.drop('preco', axis=1)
y = df['preco'].copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)

dtrain = xgboost.DMatrix(X_train, label=y_train)
dtest = xgboost.DMatrix(X_test, label=y_test)


def main():
    args = parse_arg()
    xgb_params = {
        'learning_rate': args.learning_rate,
        'max_depth': args.max_depth,
        'seed': args.seed
    }

    mlflow.set_tracking_uri('http://127.0.0.1:5000')
    mlflow.set_experiment('house-prices-script-py')

    with mlflow.start_run(run_name='XGboost'):
        mlflow.xgboost.autolog()
        xgb = xgboost.train(xgb_params, dtrain, evals=[(dtrain,'train')])

        xgb_predict = xgb.predict(dtest)

        mse = mean_squared_error(y_test, xgb_predict)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, xgb_predict)

        mlflow.log_metric('mse', mse)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('r2', r2)

if __name__ == '__main__':
    main()