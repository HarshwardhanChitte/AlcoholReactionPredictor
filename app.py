import os
import logging
from flask import Flask, render_template, request, jsonify, session
from chemistry_utils import predict_reaction, get_mol_svg

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
