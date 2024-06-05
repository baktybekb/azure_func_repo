import datetime
import logging
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'Timer triggered function ran at {utc_timestamp}')
    logging.info('_' * 200)
    print('=' * 200)