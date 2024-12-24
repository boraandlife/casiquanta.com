from flask import *





admin = Blueprint('admin', __name__, template_folder='admin')



@admin.route('/admin-panel')
def admin_panel_login():
    return render_template('tables.html')