from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import logging

# Dictionary of common alcohols and their SMILES notation
COMMON_ALCOHOLS = {
    'methanol': 'CO',
    'ethanol': 'CCO',
    'propanol': 'CCCO',
    'isopropanol': 'CC(C)O',
    'butanol': 'CCCCO',
    'isobutanol': 'CC(C)CO',
    'tert-butanol': 'CC(C)(C)O',
    'pentanol': 'CCCCCO',
    'hexanol': 'CCCCCCO',
    'phenol': 'c1ccccc1O',
    'benzyl alcohol': 'c1ccccc1CO',
    'cyclohexanol': 'C1CCCCC1O',
    'glycerol': 'C(C(CO)O)O'
}

# Dictionary of common catalysts
CATALYSTS = {
    'h2so4': 'Sulfuric Acid (H₂SO₄)',
    'h3po4': 'Phosphoric Acid (H₃PO₄)',
    'naoh': 'Sodium Hydroxide (NaOH)',
    'koh': 'Potassium Hydroxide (KOH)',
    'k2cr2o7': 'Potassium Dichromate (K₂Cr₂O₇)',
    'kmno4': 'Potassium Permanganate (KMnO₄)',
    'pcc': 'Pyridinium Chlorochromate (PCC)',
    'h2': 'Hydrogen (H₂)',
    'ni': 'Nickel (Ni)',
    'pt': 'Platinum (Pt)',
    'pd': 'Palladium (Pd)',
    'lialh4': 'Lithium Aluminum Hydride (LiAlH₄)',
    'nabh4': 'Sodium Borohydride (NaBH₄)',
    'socl2': 'Thionyl Chloride (SOCl₂)',
    'alcl3': 'Aluminum Chloride (AlCl₃)',
    'hcl': 'Hydrochloric Acid (HCl)',
    'hbr': 'Hydrobromic Acid (HBr)',
    'hi': 'Hydroiodic Acid (HI)',
    'heat': 'Heat',
    'none': 'None'
}

# Dictionary of reaction types
REACTION_TYPES = {
    'oxidation': 'Oxidation',
    'dehydration': 'Dehydration',
    'dehydrogenation': 'Dehydrogenation',
    'esterification': 'Esterification',
    'halogenation': 'Halogenation',
    'elimination': 'Elimination',
    'substitution': 'Substitution'
}

def get_mol_from_name(compound_name):
    """Convert a compound name to an RDKit molecule"""
    compound_name = compound_name.lower().strip()
    
    # Check if it's in our common alcohols
    if compound_name in COMMON_ALCOHOLS:
        smiles = COMMON_ALCOHOLS[compound_name]
        return Chem.MolFromSmiles(smiles)
    
    # Try to parse as SMILES
    try:
        mol = Chem.MolFromSmiles(compound_name)
        if mol:
            return mol
    except:
        pass
    
    # If we can't identify the compound
    return None

def get_mol_svg(compound, width=300, height=200):
    """Generate SVG for a molecule"""
    # Check if it's a SMILES string first
    try:
        mol = Chem.MolFromSmiles(compound)
        if not mol:
            mol = get_mol_from_name(compound)
    except:
        mol = get_mol_from_name(compound)
    
    if not mol:
        return f"<div class='text-danger'>Could not parse: {compound}</div>"
    
    # Generate 2D coordinates if they don't exist
    if not mol.GetNumConformers():
        AllChem.Compute2DCoords(mol)
    
    # Draw the molecule
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    
    return svg

def oxidize_alcohol(mol):
    """Oxidation reaction for alcohols"""
    smiles = Chem.MolToSmiles(mol)
    # Check for primary alcohol (RCH₂OH)
    if 'CO' in smiles and not 'C(C)(C)O' in smiles:
        # Primary alcohols oxidize to aldehydes/carboxylic acids
        if smiles == 'CO':  # Methanol
            return 'O=C=O', 'Methanol is fully oxidized to CO₂ and H₂O'
        else:
            # Replace terminal CH₂OH with CHO (aldehyde)
            aldehyde_smiles = smiles.replace('CO', 'C=O')
            # Further oxidation to carboxylic acid
            acid_smiles = smiles.replace('CO', 'C(=O)O')
            return acid_smiles, 'Primary alcohol oxidizes first to aldehyde then to carboxylic acid'
    
    # Check for secondary alcohol (R₂CHOH)
    elif 'C(C)O' in smiles or 'C(CC)O' in smiles:
        # Secondary alcohols oxidize to ketones
        ketone_smiles = smiles.replace('C(C)O', 'C(C)=O').replace('C(CC)O', 'C(CC)=O')
        return ketone_smiles, 'Secondary alcohol oxidizes to ketone'
    
    # Tertiary alcohols (R₃COH) don't easily oxidize
    elif 'C(C)(C)O' in smiles:
        return '', 'Tertiary alcohols are resistant to oxidation under normal conditions'
    
    # Phenol
    elif 'c1ccccc1O' in smiles:
        return '', 'Phenols undergo complex oxidation reactions depending on conditions'
    
    return '', 'Oxidation pathway not determined'

def dehydrate_alcohol(mol):
    """Dehydration reaction for alcohols"""
    smiles = Chem.MolToSmiles(mol)
    
    # Simple primary alcohols (except methanol)
    if 'CCO' in smiles and not 'C(C)(C)O' in smiles and smiles != 'CO':
        alkene_smiles = smiles.replace('CCO', 'C=C')
        return alkene_smiles, 'Alcohol undergoes dehydration to form an alkene'
    
    # Secondary alcohols
    elif 'C(C)O' in smiles:
        alkene_smiles = smiles.replace('C(C)O', 'C=C')
        return alkene_smiles, 'Secondary alcohol dehydrates to form an alkene'
    
    # Tertiary alcohols
    elif 'C(C)(C)O' in smiles:
        alkene_smiles = smiles.replace('C(C)(C)O', 'C=C')
        return alkene_smiles, 'Tertiary alcohol readily dehydrates to form an alkene'
    
    # Methanol can't undergo typical dehydration
    elif smiles == 'CO':
        return '', 'Methanol cannot undergo typical dehydration as it lacks a β-hydrogen'
    
    # Phenol
    elif 'c1ccccc1O' in smiles:
        return '', "Phenols generally don't undergo simple dehydration reactions"
    
    return '', 'Dehydration pathway not determined'

def halogenate_alcohol(mol, catalyst):
    """Halogenation reaction for alcohols"""
    smiles = Chem.MolToSmiles(mol)
    
    halogen = ''
    if catalyst.lower() in ['hcl', 'socl2', 'pcl5']:
        halogen = 'Cl'
        halogen_name = 'chloride'
    elif catalyst.lower() in ['hbr', 'pbr3']:
        halogen = 'Br'
        halogen_name = 'bromide'
    elif catalyst.lower() in ['hi', 'pi3']:
        halogen = 'I'
        halogen_name = 'iodide'
    else:
        return '', 'Please specify a halogenating agent (HCl, HBr, HI, SOCl₂, etc.)'
    
    # Replace OH with halogen
    if 'CO' in smiles:
        halogenated_smiles = smiles.replace('O', halogen)
        return halogenated_smiles, f'Alcohol is converted to alkyl {halogen_name}'
    
    # Phenol
    elif 'c1ccccc1O' in smiles:
        return '', 'Phenols undergo different halogenation pathways, typically at the ring positions'
    
    return '', 'Halogenation pathway not determined'

def esterify_alcohol(mol):
    """Esterification reaction for alcohols with acetic acid"""
    smiles = Chem.MolToSmiles(mol)
    
    # Replace OH with OC(=O)C for acetate ester
    if 'CO' in smiles:
        ester_smiles = smiles.replace('O', 'OC(=O)C')
        return ester_smiles, 'Alcohol reacts with acetic acid to form an acetate ester'
    
    # Phenol
    elif 'c1ccccc1O' in smiles:
        ester_smiles = 'CC(=O)Oc1ccccc1'
        return ester_smiles, 'Phenol reacts with acetic acid to form phenyl acetate'
    
    return '', 'Esterification pathway not determined'

def predict_reaction(compound, catalyst, reaction_type):
    """Predict the products of alcohol/phenol reactions"""
    try:
        # Convert compound names to SMILES for RDKit processing
        if compound.lower() in COMMON_ALCOHOLS:
            smiles = COMMON_ALCOHOLS[compound.lower()]
            mol = Chem.MolFromSmiles(smiles)
        else:
            # Try to interpret as SMILES directly
            mol = Chem.MolFromSmiles(compound)
            
        if not mol:
            return {
                'success': False,
                'error': f"Couldn't recognize or parse the compound: {compound}"
            }
        
        # Get canonical SMILES from the molecule for consistency
        smiles = Chem.MolToSmiles(mol)
        
        # Check if the molecule contains an alcohol group
        if 'O' not in smiles and 'OH' not in smiles:
            return {
                'success': False,
                'error': f"The compound doesn't appear to be an alcohol or phenol: {compound}"
            }
        
        # Check if it's phenol
        is_phenol = smiles == 'c1ccccc1O' or smiles == 'Oc1ccccc1'
        
        # Different reaction pathways
        product_smiles = ''
        details = ''
        
        # Phenol-specific reactions
        if is_phenol:
            if reaction_type == 'oxidation':
                if catalyst.lower() in ['k2cr2o7', 'kmno4']:
                    product_smiles = 'O=C1C=CC(=O)C=C1'  # Benzoquinone
                    details = 'Phenol undergoes oxidation to form benzoquinone under strong oxidizing conditions'
                else:
                    return {
                        'success': False,
                        'error': "Phenol oxidation requires a strong oxidizing agent like K₂Cr₂O₇ or KMnO₄"
                    }
            elif reaction_type == 'halogenation':
                if catalyst.lower() in ['hcl', 'hbr', 'hi']:
                    # Electrophilic aromatic substitution occurs at ortho/para positions
                    halogen = ''
                    if catalyst.lower() == 'hcl':
                        halogen = 'Cl'
                        halogen_name = 'chlorophenol'
                    elif catalyst.lower() == 'hbr':
                        halogen = 'Br'
                        halogen_name = 'bromophenol'
                    elif catalyst.lower() == 'hi':
                        halogen = 'I'
                        halogen_name = 'iodophenol'
                    
                    # 2,4,6-trihalogenated phenol is typically the major product
                    if halogen == 'Cl':
                        product_smiles = 'Oc1c(Cl)cc(Cl)cc1Cl'  # 2,4,6-trichlorophenol
                    elif halogen == 'Br':
                        product_smiles = 'Oc1c(Br)cc(Br)cc1Br'  # 2,4,6-tribromophenol
                    elif halogen == 'I':
                        product_smiles = 'Oc1c(I)cc(I)cc1I'  # 2,4,6-triiodophenol
                    
                    details = f'Phenol undergoes halogenation to form multiple {halogen_name} products, with 2,4,6-tri{halogen_name} as the major product'
                else:
                    return {
                        'success': False,
                        'error': "Phenol halogenation requires a halogen donor like HCl, HBr, or HI"
                    }
            elif reaction_type == 'esterification':
                if catalyst.lower() in ['h2so4', 'h3po4']:
                    product_smiles = 'CC(=O)Oc1ccccc1'  # Phenyl acetate
                    details = 'Phenol reacts with acetic acid to form phenyl acetate in the presence of an acid catalyst'
                else:
                    return {
                        'success': False,
                        'error': "Phenol esterification requires an acid catalyst like H₂SO₄ or H₃PO₄"
                    }
            elif reaction_type == 'dehydration':
                return {
                    'success': False,
                    'error': "Phenol doesn't undergo typical dehydration reactions like aliphatic alcohols. The aromatic ring stabilizes the C-O bond."
                }
        else:
            # Regular alcohol reactions
            if reaction_type == 'oxidation':
                if catalyst.lower() in ['k2cr2o7', 'kmno4', 'pcc']:
                    product_smiles, details = oxidize_alcohol(mol)
                else:
                    return {
                        'success': False,
                        'error': "Oxidation typically requires an oxidizing agent like K₂Cr₂O₇, KMnO₄, or PCC"
                    }
                    
            elif reaction_type == 'dehydration':
                if catalyst.lower() in ['h2so4', 'h3po4', 'heat']:
                    product_smiles, details = dehydrate_alcohol(mol)
                else:
                    return {
                        'success': False,
                        'error': "Dehydration typically requires an acid catalyst like H₂SO₄ or H₃PO₄, or heat"
                    }
                    
            elif reaction_type == 'halogenation':
                product_smiles, details = halogenate_alcohol(mol, catalyst)
                
            elif reaction_type == 'esterification':
                if catalyst.lower() in ['h2so4', 'h3po4']:
                    product_smiles, details = esterify_alcohol(mol)
                else:
                    return {
                        'success': False,
                        'error': "Esterification typically requires an acid catalyst like H₂SO₄"
                    }
            
            else:
                return {
                    'success': False,
                    'error': f"Reaction type '{reaction_type}' not supported yet"
                }
        
        if not product_smiles:
            return {
                'success': False,
                'error': details or "Couldn't determine reaction product"
            }
            
        # Try to convert SMILES to a more readable name
        try:
            product_mol = Chem.MolFromSmiles(product_smiles)
            if product_mol:
                return {
                    'success': True,
                    'product': product_smiles,
                    'details': details
                }
        except Exception as e:
            logging.error(f"Error converting product SMILES: {str(e)}")
            
        return {
            'success': True,
            'product': product_smiles,
            'details': details
        }
            
    except Exception as e:
        logging.error(f"Error in reaction prediction: {str(e)}")
        return {
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }

def get_common_alcohols():
    """Return a list of common alcohols for suggestions"""
    return sorted(list(COMMON_ALCOHOLS.keys()))

def get_catalysts():
    """Return a list of catalysts"""
    return CATALYSTS

def get_reaction_types():
    """Return a list of reaction types"""
    return REACTION_TYPES
