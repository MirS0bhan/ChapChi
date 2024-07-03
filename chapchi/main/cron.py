# my crons

from .tasks import delete_old_files

def delelet_old_files_hourly():
    delete_old_files()
    