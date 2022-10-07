from waitress import serve
import myapp
serve(myapp.app, host='0.0.0.0', port=5050)
