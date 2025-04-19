import os
import logging
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from chemistry_utils import predict_reaction, get_mol_svg, get_common_alcohols, get_catalysts, get_reaction_types
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db = SQLAlchemy(app)

# Import models after db is defined
from models import Reaction

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        compound = request.form.get('compound', '')
        catalyst = request.form.get('catalyst', '')
        reaction_type = request.form.get('reaction_type', '')
        save_to_db = request.form.get('save_to_db') == 'true'
        
        if not compound:
            return jsonify({
                'success': False,
                'error': 'Please enter a compound'
            })
            
        # Predict reaction
        result = predict_reaction(compound, catalyst, reaction_type)
        
        if not result['success']:
            return jsonify(result)
            
        # Get molecule visualizations
        reactant_svg = get_mol_svg(compound)
        product_svg = get_mol_svg(result['product']) if result['product'] else ''
        
        # Save to database if requested
        if save_to_db:
            try:
                reaction = Reaction(
                    reactant=compound,
                    catalyst=catalyst,
                    reaction_type=reaction_type,
                    product=result['product'],
                    details=result['details']
                )
                db.session.add(reaction)
                db.session.commit()
                logging.info(f"Saved reaction to database: {reaction}")
            except Exception as db_error:
                logging.error(f"Error saving to database: {str(db_error)}")
        
        return jsonify({
            'success': True,
            'reactant': compound,
            'reactant_svg': reactant_svg,
            'catalyst': catalyst,
            'reaction_type': reaction_type,
            'product': result['product'],
            'product_svg': product_svg,
            'reaction_details': result['details']
        })
        
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/history', methods=['GET'])
def get_history():
    try:
        reactions = Reaction.query.order_by(Reaction.created_at.desc()).limit(50).all()
        return jsonify({
            'success': True,
            'reactions': [reaction.to_dict() for reaction in reactions]
        })
    except Exception as e:
        logging.error(f"Error retrieving history: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/history/view', methods=['GET'])
def view_history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
