import wsgiserver
from flask import Flask, url_for, jsonify

from predictor.services.cleandirty import clean_dirty

app = Flask(__name__)
app.register_blueprint(clean_dirty)


@app.route("/site-map")
def site_map():
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return jsonify(links)


def main():
    http_server = wsgiserver.WSGIServer(app, host='0.0.0.0', port=8181)
    http_server.start()


if __name__ == '__main__':
    main()