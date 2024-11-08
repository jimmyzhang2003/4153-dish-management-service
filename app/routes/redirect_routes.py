from flask import Blueprint, redirect

# register blueprint
redirect_bp = Blueprint('redirect', __name__)

# GET /: Redirect to Swagger page
@redirect_bp.route('/', methods=['GET'])
def root():
    return redirect("/apidocs", code=302)

# GET /api/v1/: Redirect to Swagger page
@redirect_bp.route('/api/v1/', methods=['GET'])
def api_root():
    return redirect("/apidocs", code=302)