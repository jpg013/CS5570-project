#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, send_from_directory
import os

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__, static_folder='web-ui/build')
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Serve index.html for root
#----------------------------------------------------------------------------#

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("web-ui/build/" + path):
        return send_from_directory('web-ui/build', path)
    else:
        return send_from_directory('web-ui/build', 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=True)

