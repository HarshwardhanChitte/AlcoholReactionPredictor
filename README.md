# ChemReact: Alcohol & Phenol Reaction Predictor

ChemReact is a Flask-based web application designed to predict chemical reaction products for alcohols and phenols. Users can input chemical compounds using common names or SMILES notation, select catalysts, and view predicted products with high-quality molecular structure visualizations.

## 🚀 Features

- **Reaction Prediction**: Predicts products for common alcohol and phenol reactions (e.g., oxidation, esterification).
- **Flexible Input**: Supports both common chemical names (e.g., "ethanol", "phenol") and SMILES notation.
- **Molecular Visualization**: Generates SVG visualizations of molecular structures using RDKit.
- **Reaction History**: Save your predicted reactions to a PostgreSQL database and view them later.
- **Dark Mode UI**: Clean, responsive interface built with Bootstrap.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Chemistry Engine**: RDKit (Cheminformatics toolkit)
- **Frontend**: Jinja2 templates, Bootstrap 5, FontAwesome
- **Server**: Gunicorn

## 📋 Prerequisites

To run this project locally, you will need:
- Python 3.11+
- PostgreSQL
- RDKit (can be installed via `pip install rdkit`)

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/alcohol-phenol-predictor.git
   cd alcohol-phenol-predictor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file or set the following variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SESSION_SECRET`: A secret key for Flask sessions

4. **Run the application**:
   ```bash
   python main.py
   ```
   The app will be available at `http://localhost:5000`.

## 📁 Project Structure

- `app.py`: Flask application factory and route definitions.
- `models.py`: Database models for storing reactions.
- `chemistry_utils.py`: Logic for chemical reaction prediction and visualization.
- `templates/`: HTML templates for the web interface.
- `static/`: CSS and JavaScript files.

## 📜 License

© 2025 Chemistry Predictor App. All rights reserved.
