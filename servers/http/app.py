from flask import Flask
from flask_restful import Resource, Api

# Resources
# from resources.mini import resources as mini_resources

from resources import all as resource_set

app = Flask(__name__)
api = Api(app)

for resources in resource_set:
    for resource in resources:
        api.add_resource(*resource)

if __name__ == '__main__':
    app.run(debug=True)
