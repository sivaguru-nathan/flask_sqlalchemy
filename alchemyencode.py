from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime
import decimal

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field]=data.isoformat()
                    elif isinstance(obj, decimal.Decimal):
                        fields[field] = float(obj)
                    else :
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)