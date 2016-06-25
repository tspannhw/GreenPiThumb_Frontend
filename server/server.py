#!/usr/bin/python2
"""Web server for GreenPiThumb."""

import argparse
import json

import klein
from twisted.web.static import File

import dummy_values


def main(args):
    app = klein.Klein()

    # TODO(mtlynch): Replace all history routes with real values once the
    # non-dummy data is available.
    @app.route('/temperatureHistory.json')
    def temperature_history(request):
        return json.dumps(dummy_values.generate_values('temperature', 34.2,
                                                       5.0))

    @app.route('/reservoirHistory.json')
    def reservoir_history(request):
        return json.dumps(dummy_values.generate_values('water_ml', 1989.2,
                                                       14.0))

    @app.route('/lightHistory.json')
    def light_history(request):
        return json.dumps(dummy_values.generate_values('light_pct', 57.4, 3.0))

    @app.route('/soilMoistureHistory.json')
    def soil_moisture_history(request):
        return json.dumps(dummy_values.generate_values('moisture', 105.9, 4.0))

    @app.route('/ambientHumidityHistory.json')
    def ambient_humidity_history(request):
        return json.dumps(dummy_values.generate_values('humidity', 87.3, 6.0))

    # TODO(mtlynch): It might make more sense to bring nginx into this stack so
    # that nginx handles static files and Python just handles things that have
    # to be calculated on the fly. This is okay for now, though.
    @app.route('/dashboard')
    def home(request):
        return File('./static/dashboard.html')

    @app.route('/static/', branch=True)
    def static(request):
        return File('./static')

    app.run('0.0.0.0', args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GreenPiThumb Web Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, default=8888)
    main(parser.parse_args())