# Alcohol & Phenol Reaction Predictor

## Overview

This is a Flask-based web application that predicts chemical reactions involving alcohols and phenols. The application allows users to input chemical compounds (either by name or SMILES notation), select catalysts and reaction types, and view predicted reaction products with molecular structure visualizations. Users can save reactions to a database and view their reaction history.

## System Architecture

The application follows a traditional Flask MVC pattern with the following key architectural decisions:

**Frontend**: Server-side rendered HTML templates using Jinja2 with Bootstrap for responsive UI and JavaScript for dynamic interactions
- **Rationale**: Simple deployment and maintenance, good for chemistry visualization needs
- **Alternatives**: Could use React/Vue for SPA, but server-side rendering is sufficient for this use case

**Backend**: Flask web framework with SQLAlchemy ORM
- **Rationale**: Lightweight, well-suited for scientific applications, good RDKit integration
- **Pros**: Fast development, excellent chemistry library support
- **Cons**: Single-threaded by default (mitigated by Gunicorn in production)

**Database**: PostgreSQL with SQLAlchemy ORM
- **Rationale**: Robust relational database with good Flask integration
- **Alternatives**: SQLite for development, but PostgreSQL provides better production scalability

**Chemistry Engine**: RDKit for molecular structure processing and visualization
- **Rationale**: Industry standard for cheminformatics, excellent SMILES support
- **Pros**: Comprehensive chemistry toolkit, SVG generation
- **Cons**: Large dependency, but essential for chemistry applications

## Key Components

### Flask Application (`app.py`)
- Main application factory and route definitions
- Database configuration and initialization
- Session management with configurable secret key
- Integration with chemistry utilities

### Chemistry Utilities (`chemistry_utils.py`)
- RDKit-based molecular structure processing
- SMILES notation handling and validation
- SVG generation for molecular visualization
- Predefined chemical compound and catalyst databases
- Reaction prediction logic

### Data Models (`models.py`)
- SQLAlchemy model for storing reaction data
- Includes reactants, products, catalysts, reaction types
- Timestamp tracking and JSON serialization support

### Frontend Templates
- `layout.html`: Base template with Bootstrap dark theme
- `index.html`: Main reaction prediction interface
- `history.html`: Reaction history viewing interface
- Responsive design with FontAwesome icons

### Static Assets
- `script.js`: Frontend JavaScript for form handling and AJAX requests
- `style.css`: Custom CSS for chemistry-specific styling

## Data Flow

1. **User Input**: User enters compound name/SMILES, selects catalyst and reaction type
2. **Validation**: Frontend validates input, chemistry_utils validates chemical structures
3. **Prediction**: RDKit processes molecular structures and predicts reaction products
4. **Visualization**: SVG molecular structures generated for display
5. **Storage**: Optional saving of reaction data to PostgreSQL database
6. **History**: Users can view previously saved reactions

## External Dependencies

### Core Dependencies
- **Flask 3.1.0+**: Web framework
- **RDKit 2024.9.6+**: Chemistry toolkit for molecular processing
- **PostgreSQL**: Database system with psycopg2-binary driver
- **SQLAlchemy 3.1.1+**: ORM for database operations
- **Gunicorn 23.0.0+**: WSGI server for production deployment

### Frontend Dependencies
- **Bootstrap**: UI framework (via CDN)
- **FontAwesome**: Icon library (via CDN)
- **Replit Bootstrap Theme**: Custom dark theme

### System Dependencies (via Nix)
- **PostgreSQL 16**: Database server
- **Python 3.11**: Runtime environment
- **Various chemistry libraries**: Cairo, Eigen, InChI, RapidJSON for RDKit support

## Deployment Strategy

**Development**: 
- Flask development server with debug mode
- SQLite or PostgreSQL development database
- Hot reload enabled

**Production**: 
- Gunicorn WSGI server with multiple workers
- PostgreSQL database with connection pooling
- Replit autoscale deployment target
- Environment variable configuration for secrets
- Port 5000 internal, port 80 external

**Configuration Management**:
- Environment variables for database URLs and secrets
- `pyproject.toml` for Python dependencies
- `.replit` file for Replit-specific configuration
- Nix packages for system-level dependencies

The deployment uses Gunicorn with `--reuse-port` and `--reload` flags for better performance and development experience.

## Changelog

```
Changelog:
- June 15, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```