import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.transaction import TransactionHandler

class IssueHandler(TransactionHandler):

    # Default constructor for the Issue handler
    def __init__(self, db_name='default'):
        TransactionHandler.__init__(self, db_name)

    # Creates new record in the database for the issue
    def create(self, title, type, number, file, date):
        # Analyzed is false by default when creating a new issue
        values = {'title' : title, 'type' : type, 'number' : number, 'file' : file, 'date' : date, 'analyzed': 0}
        TransactionHandler.insert(self, 'issues', values)

    # Loads information about an issue by its title
    def load_by_title(self, title):
        conditions = {'title' : [title]}
        return TransactionHandler.select_one(self, table='issues', conditions=conditions)

    # Loads all issues
    def load_all(self, conditions=None, group_by=None, joins=None):
        return TransactionHandler.select_all(self, table='issues', conditions=conditions, joins=joins, group_by=group_by)

    # Loads a random issue
    def load_random(self, conditions=None):
        return TransactionHandler.select_random(self, table='issues', conditions=conditions)

    # Given an issue's id, indicates it has been analyzed
    def set_analyzed(self, issue_id):
        params = {'analyzed': 1}
        conditions = {'id' : [issue_id]}
        TransactionHandler.update(self, table='issues', params=params, conditions=conditions)
