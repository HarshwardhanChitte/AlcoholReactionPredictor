from datetime import datetime
from app import db

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reactant = db.Column(db.String(100), nullable=False)
    reactant_smiles = db.Column(db.String(200))
    catalyst = db.Column(db.String(100), nullable=False)
    reaction_type = db.Column(db.String(50), nullable=False)
    product = db.Column(db.String(200))
    product_smiles = db.Column(db.String(200))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reaction {self.reactant} + {self.catalyst} ({self.reaction_type})>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'reactant': self.reactant,
            'reactant_smiles': self.reactant_smiles,
            'catalyst': self.catalyst,
            'reaction_type': self.reaction_type,
            'product': self.product,
            'product_smiles': self.product_smiles,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }