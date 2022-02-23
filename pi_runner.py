from dbaccessor import DBAccessor
from detector import Detector
import config


def main():
    usr = config.mysql['user']
    pwd = config.mysql['password']
    hst = config.mysql['host']
    db = usr+'_DB'

    access = DBAccessor(usr, pwd, hst, db)
    det = Detector(access)
    det.run()
main()
