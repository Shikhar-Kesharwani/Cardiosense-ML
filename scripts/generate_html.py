import os

brfss_cols = ['BPHIGH4', 'TOLDHI2', 'CHOLCHK', 'SMOKE100', 'CVDSTRK3', 'DIABETE3', '_TOTINDA', '_FRTLT1', '_VEGLT1', 'HLTHPLN1', 'MEDCOST', 'GENHLTH', 'MENTHLTH', 'PHYSHLTH', 'DIFFWALK', 'SEX', '_AGEG5YR', 'EDUCA', 'INCOME2', 'ASTHMA3', 'CHCSCNCR', 'CHCOCNCR', 'CHCCOPD1', 'HAVARTH3', 'ADDEPEV2', 'CHCKIDNY', 'WEIGHT2', 'HEIGHT3', 'ALCDAY5', 'EXERANY2', 'SEATBELT', 'FLUSHOT6', 'PNEUVAC3', 'HIVTST6', 'QSTVER', 'QSTLANG', '_STATE', 'MSCODE', 'MARITAL', 'VETERAN3', 'DECIDE', 'DIFFALON']

uci_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

with open('brfss_form.html', 'w') as f:
    for col in brfss_cols:
        f.write(f'''
<div class="form-group">
    <label for="{col}">{col}</label>
    <input type="number" name="{col}" id="{col}" required placeholder="0">
</div>
''')

with open('uci_form.html', 'w') as f:
    for col in uci_cols:
        f.write(f'''
<div class="form-group">
    <label for="{col}">{col}</label>
    <input type="number" step="0.1" name="{col}" id="{col}" required placeholder="0">
</div>
''')
