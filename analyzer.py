class Analyzer:
    def __init__(self, accessor):
        self.database_access = accessor

    def execute_query(self, qy, vals = None):
        if vals == None:
            self.database_access.query_db(qy)
        else:
            self.database_access.query_db(qy, vals)

        result = self.database_access.get_rs()
        return result

    def get_number_of_walk_ins(self):
        qy = '''SELECT COUNT(*) FROM Walk_In'''
        return self.execute_query(qy)

    def get_number_of_walk_ins_between_times(self, lower, upper):
        qy = '''SELECT COUNT(*) FROM Walk_In w WHERE w.enter_time BETWEEN CAST(%s AS TIME) AND CAST(%s AS TIME)'''
        return self.execute_query(qy, (lower, upper))
   
    def get_number_of_walk_ins_by_service(self, order, service=None):
        qy = ''''''
        if service is not None:
            qy = '''SELECT t.service, COUNT(w.height) FROM Walk_In w JOIN Ticket t USING (height, enter_time, enter_date, exit_time, exit_date) GROUP BY t.service HAVING t.service = %s'''
            return self.execute_query(qy, (service))
        else:
            qy = '''SELECT t.service, COUNT(w.height) FROM Walk_In w JOIN Ticket t USING (height, enter_time, enter_date, exit_time, exit_date) GROUP BY t.service ORDER BY COUNT(w.height) DESC'''
            return self.execute_query(qy)

    def average_time_spent_inside_by_service(self, order, service=None):
        qy = ''''''
        if service is not None:
            qy = '''SELECT t.service, AVG(w.exit_time - w.enter_time) AS avg_time FROM Walk_In w JOIN Ticket t USING (height, enter_time, enter_date, exit_time, exit_date) GROUP BY t.service HAVING t.service = %s'''
            return self.execute_query(qy, (service))
        else:
            qy = '''SELECT t.service, AVG(w.exit_time - w.enter_time) AS avg_time FROM Walk_In w JOIN Ticket t USING (height, enter_time, enter_date, exit_time, exit_date) GROUP BY t.service ORDER BY AVG(w.exit_time - w.enter_time) '''+order
            return self.execute_query(qy)

    def get_tickets(self):
        qy = '''SELECT * FROM Ticket'''
        return self.execute_query(qy)
    
    def get_tickets_filtered(self, id_num=None, status=None, service=None, subject=None, description=None, requestor=None, responsible=None, height=None, enter_time=None, enter_date=None, exit_time=None, exit_date=None, last_modifier=None):
        filter_dict = {   
            '''id_num''':id_num,
            '''status''':status,
            '''service''':service,
            '''subject''':subject,
            '''description''':description,
            '''requestor''':requestor,
            '''responsible''':responsible,
            '''height''':height,
            '''enter_time''':enter_time,
            '''enter_date''':enter_date,
            '''exit_time''':exit_time,
            '''exit_date''':exit_date,
            '''last_modifier''':last_modifier}
        where_clause = ''''''
        i = 0
        vals = []
        for k,v in filter_dict.items():
            if v is not '':
                where_clause+= (''' AND ''' if i != 0 else ''' ''')+k+'''= %s'''
                vals.append(v)
                i += 1
        print(where_clause)
        qy = '''SELECT * FROM Ticket WHERE '''+where_clause 
        return self.execute_query(qy, tuple(vals))

    def get_number_of_tickets_mod_by_user(self, order, user=None):
        qy = '''SELECT u.username, COUNT(u.ticket_id) FROM User_Modified u JOIN Ticket t using (ticket_id) GROUP BY u.username''' +(''' HAVING u.username='''+user if user is not None else '''''')+''' ORDER BY '''+order
        return self.execute_query(qy)
    
    def get_number_of_tickets_closed_or_resolved_by_user(self, order, user=None):
        qy = '''SELECT up.username, COUNT(up.ticket_id) FROM User_Profile up JOIN User_Modified u USING (username) JOIN Ticket t USING (ticket_id) 
                WHERE t.last_modifier = up.username GROUP BY up.username''' +(''' HAVING up.username='''+user if user is not None else '''''')+''' ORDER BY '''+order
        return self.execute_query(qy)




        
