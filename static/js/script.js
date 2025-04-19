document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reaction-form');
    const loadingIndicator = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const resultsContainer = document.getElementById('results-container');
    const initialMessage = document.getElementById('initial-message');
    
    // Common alcohols for the dropdown
    const commonAlcohols = [
        'methanol',
        'ethanol',
        'propanol',
        'isopropanol',
        'butanol',
        'tert-butanol',
        'phenol',
        'benzyl alcohol',
        'cyclohexanol',
        'glycerol'
    ];
    
    // Populate alcohol examples dropdown
    const alcoholExamples = document.getElementById('alcohol-examples');
    commonAlcohols.forEach(alcohol => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.classList.add('dropdown-item');
        a.textContent = alcohol;
        a.href = '#';
        a.addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('compound').value = alcohol;
        });
        li.appendChild(a);
        alcoholExamples.appendChild(li);
    });
    
    // Reaction types
    const reactionTypes = {
        'oxidation': 'Oxidation',
        'dehydration': 'Dehydration',
        'halogenation': 'Halogenation',
        'esterification': 'Esterification'
    };
    
    // Populate reaction type dropdown
    const reactionTypeSelect = document.getElementById('reaction_type');
    for (const [value, text] of Object.entries(reactionTypes)) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        reactionTypeSelect.appendChild(option);
    }
    
    // Catalysts/reagents
    const catalysts = {
        'h2so4': 'Sulfuric Acid (H₂SO₄)',
        'h3po4': 'Phosphoric Acid (H₃PO₄)',
        'kmno4': 'Potassium Permanganate (KMnO₄)',
        'k2cr2o7': 'Potassium Dichromate (K₂Cr₂O₇)',
        'pcc': 'Pyridinium Chlorochromate (PCC)',
        'hcl': 'Hydrochloric Acid (HCl)',
        'hbr': 'Hydrobromic Acid (HBr)',
        'hi': 'Hydroiodic Acid (HI)',
        'socl2': 'Thionyl Chloride (SOCl₂)',
        'heat': 'Heat',
        'naoh': 'Sodium Hydroxide (NaOH)'
    };
    
    // Populate catalyst dropdown
    const catalystSelect = document.getElementById('catalyst');
    for (const [value, text] of Object.entries(catalysts)) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        catalystSelect.appendChild(option);
    }
    
    // Dynamic catalyst options based on reaction type
    reactionTypeSelect.addEventListener('change', function() {
        const selectedReaction = this.value;
        catalystSelect.innerHTML = '<option value="" selected disabled>Select catalyst/reagent</option>';
        
        // Filter catalysts based on reaction type
        let relevantCatalysts = {};
        
        if (selectedReaction === 'oxidation') {
            relevantCatalysts = {
                'kmno4': 'Potassium Permanganate (KMnO₄)',
                'k2cr2o7': 'Potassium Dichromate (K₂Cr₂O₇)',
                'pcc': 'Pyridinium Chlorochromate (PCC)'
            };
        } else if (selectedReaction === 'dehydration') {
            relevantCatalysts = {
                'h2so4': 'Sulfuric Acid (H₂SO₄)',
                'h3po4': 'Phosphoric Acid (H₃PO₄)',
                'heat': 'Heat'
            };
        } else if (selectedReaction === 'halogenation') {
            relevantCatalysts = {
                'hcl': 'Hydrochloric Acid (HCl)',
                'hbr': 'Hydrobromic Acid (HBr)',
                'hi': 'Hydroiodic Acid (HI)',
                'socl2': 'Thionyl Chloride (SOCl₂)'
            };
        } else if (selectedReaction === 'esterification') {
            relevantCatalysts = {
                'h2so4': 'Sulfuric Acid (H₂SO₄)',
                'h3po4': 'Phosphoric Acid (H₃PO₄)'
            };
        }
        
        // Add the filtered catalysts to the dropdown
        for (const [value, text] of Object.entries(relevantCatalysts)) {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = text;
            catalystSelect.appendChild(option);
        }
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        
        // Show loading, hide results and errors
        loadingIndicator.classList.remove('d-none');
        errorMessage.classList.add('d-none');
        resultsContainer.classList.add('d-none');
        initialMessage.classList.add('d-none');
        
        // Send the request
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            loadingIndicator.classList.add('d-none');
            
            if (data.success) {
                // Show results
                resultsContainer.classList.remove('d-none');
                
                // Update reactant information
                document.getElementById('reactant-structure').innerHTML = data.reactant_svg;
                document.getElementById('reactant-name').textContent = data.reactant;
                
                // Update product information
                if (data.product_svg) {
                    document.getElementById('product-structure').innerHTML = data.product_svg;
                    document.getElementById('product-name').textContent = data.product;
                } else {
                    document.getElementById('product-structure').innerHTML = '<div class="alert alert-warning">No product visualization available</div>';
                    document.getElementById('product-name').textContent = data.product || 'No product';
                }
                
                // Update reaction details
                document.getElementById('result-reaction-type').textContent = reactionTypes[data.reaction_type] || data.reaction_type;
                document.getElementById('result-catalyst').textContent = catalysts[data.catalyst] || data.catalyst;
                document.getElementById('reaction-details').textContent = data.reaction_details || 'No detailed information available.';
            } else {
                // Show error
                errorMessage.classList.remove('d-none');
                errorText.textContent = data.error || 'An unknown error occurred.';
            }
        })
        .catch(error => {
            // Hide loading
            loadingIndicator.classList.add('d-none');
            
            // Show error
            errorMessage.classList.remove('d-none');
            errorText.textContent = 'Network error: ' + error.message;
            console.error('Error:', error);
        });
    });
});
