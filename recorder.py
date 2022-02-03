class Recorder:
    def __init__(self, accessor):
        self.database_access = accessor
    
    def record_walk_in(self, height, enter_time, enter_date):
        table = "Walk_In"
        values = [str(height), enter_time, enter_date]
        cols = ['height', 'enter_time', 'enter_date']
        self.insert_plain(table, cols, values)

    def add_walk_in_time_out(self, height, enter_time, enter_date, exit_time, exit_date):
        table = 'Walk_In'
        set_cols_and_vals = {'exit_time':str(exit_time), 'exit_date':str(exit_date)}
        where_cols_ops_vals_connect = {('height', '='):(str(height), 'AND'), ('enter_time', '='):(str(enter_time), 'AND'), ('enter_date', '='):(str(enter_date),'AND'), ('exit_time', 'is'):('NULL', '')}
        self.update_plain(table, set_cols_and_vals, where_cols_ops_vals_connect)

    def update_plain(self, table, set_cols_and_vals, where_cols_ops_vals_connect): 
        # UPDATE table_name
        # SET column1 = value1, column2 = value2, ...
        # WHERE condition;
        qy = "UPDATE "+table+" SET "
        for k,v in set_cols_and_vals.items():
            qy += k+'='+v+', '
        qy = qy[:-2]+' WHERE '
        for k,v in where_cols_ops_vals_connect.items():
            qy += k[0]+k[1]+v[0]+' '+v[1]+' '
        qy = qy[:-2]+';'
        self.database_access.query_db(qy)

    def insert_plain(self, table, cols, values):

        qy = "INSERT INTO "+table+" (" 
        for col in cols:
            qy += col+', '
        qy = qy[:-2]+') Values('
        for value in values: 
            qy += "%s, "
        qy = qy[:-2]+");"
        self.database_access.query_db(qy, tuple(values))


        
