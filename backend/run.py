from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from Model import RevokedTokenModel


def create_app(config_filename):
    app = Flask(__name__)
    # flask_cors.CORS(app, expose_headers='Authorization')
    app.config.from_object(config_filename)

    from app import api_bp

    # Legger til CORS-funksjonalitet. Har ikke peiling hvordan det fungerer
    CORS(api_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import db
    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    # Legger til en melding som blir sendt om en bruker prøver å logge på med en utgått token.
    @jwt.revoked_token_loader
    def my_revoked_token_callback():
        return jsonify({
            'status': 401,
            'sub_status': 43,
            'msg': 'The token has been revoked. Try to login again for renewed access.'
        }), 401

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'msg': 'The token has expired. Try to login again for renewed access.'
        }), 401

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
