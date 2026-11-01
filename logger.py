from datetime import datetime

def log_info(message:str):
    print(f'\nINFO | {datetime.now().strftime('%H:%M:%S')} -> {message}')

def log_warning(message:str):
    print(f'\nWARNING | {datetime.now().strftime('%H:%M:%S')} -> {message}')

def log_error(message:str):
    print(f'\nERROR | {datetime.now().strftime('%H:%M:%S')} -> {message}')

def log_step(title:str):
    print('\n' + '=' * 60)
    print(title.upper())
    print('=' * 60)
