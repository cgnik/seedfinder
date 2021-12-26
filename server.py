import os

from flask import Flask, send_from_directory, Response, request, redirect, flash, abort, jsonify, make_response
from werkzeug.utils import secure_filename

from seeds import seeds_geds


def _server():
    app = Flask(__name__)
    app.static_url_path = 'html'
    app.static_folder = os.path.join(app.root_path, app.static_url_path)
    app.config['UPLOAD_FOLDER'] = os.environ.get('SEEDS_FOLDER', '/tmp')

    def _allowed_file(filename):
        return filename is not None and '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv']

    def _get_file(file_key):
        if file_key in request.files and request.files[file_key].filename != '':
            file = request.files[file_key]
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_name)
            return file_name
        return None

    @app.route("/", defaults={'file_name': ''})
    @app.route("/<path:file_name>")
    def static_file(file_name: str):
        if not file_name:
            return send_from_directory('html', 'index.html')
        if os.path.exists(os.path.join(app.static_url_path, file_name)):
            return send_from_directory('html', file_name)
        abort(Response('Not found', 404))

    @app.route("/seeds-ged", methods=['POST'])
    def seeds_geds_process():
        seeds, geds = None, None
        try:
            seeds = _get_file('seeds_file')
            geds = _get_file('ged_file')
            if not seeds or not geds:
                flash('Must provide both seeds and GED csv files')
                return redirect(request.url)
            if not _allowed_file(seeds) or not _allowed_file(geds):
                flash('Both seeds and GED files must be csv files')
                return redirect(request.url)
            rows = seeds_geds(seeds, geds, int(request.form.get('threshold')))
            result = {"{}, {}. {}".format(*row['Closest Match']): f"{row['Last']}, {row['First']}. DoB {row['DoB']}"
                      for i, row in
                      rows.iterrows()}
            r = jsonify(result)
            return r
        except Exception as e:
            print(e)
        finally:
            if seeds:
                os.remove(seeds)
            if geds:
                os.remove(geds)
        return make_response(500, 'Server error')

    return app


if __name__ == '__main__':
    _server().run('0.0.0.0', int(os.environ.get('SEEDS_PORT', '8080')))
