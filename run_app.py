from recorder import Recorder
from dbaccessor import DBAccessor
from analyzer import Analyzer
from client_side import GUI
import config
import mysql.connector

def main():
    usr = config.mysql['user']
    pwd = config.mysql['password']
    hst = config.mysql['host']
    db = usr+'_DB'

    access = DBAccessor(usr, pwd, hst, db)
    analysis = Analyzer(access)
    recorder = Recorder(access)

    main_page = GUI(access, analysis, recorder)
    main_page.front_page()

if __name__ == '__main__':
    main()
