import os

with open('templates/index.html', 'r') as f:
    content = f.read()

# Replace the buttons
new_buttons = """
            <div class="toggle-container" style="flex-wrap: wrap;">
                <button id="btn-cdc" class="toggle-btn active" onclick="toggleForm('cdc')">Mode 1: Quick Public Health</button>
                <button id="btn-clinical" class="toggle-btn" onclick="toggleForm('clinical')">Mode 2: Basic Physical</button>
                <button id="btn-uci" class="toggle-btn" onclick="toggleForm('uci')">Mode 3: Advanced Lab Diagnosis</button>
                <button id="btn-brfss" class="toggle-btn" onclick="toggleForm('brfss')">Mode 4: Deep Lifestyle Analysis</button>
            </div>
"""

# Find the toggle container
start_toggle = content.find('<div class="toggle-container">')
end_toggle = content.find('</div>', start_toggle) + 6
content = content[:start_toggle] + new_buttons + content[end_toggle:]

# Now, read uci_form.html and brfss_form.html
with open('uci_form.html', 'r') as f:
    uci_form_content = f.read()

with open('brfss_form.html', 'r') as f:
    brfss_form_content = f.read()

new_forms = f"""
            <!-- UCI FORM -->
            <form action="/predict_uci" method="post" class="grid-form" id="uci-form" style="display: none;">
                {uci_form_content}
                <div class="form-actions full-width">
                    <button type="submit" class="glow-button">
                        <i class="fa-solid fa-microchip"></i> Analyze Advanced Labs
                    </button>
                </div>
            </form>

            <!-- BRFSS FORM -->
            <form action="/predict_brfss" method="post" class="grid-form" id="brfss-form" style="display: none;">
                {brfss_form_content}
                <div class="form-actions full-width">
                    <button type="submit" class="glow-button">
                        <i class="fa-solid fa-microchip"></i> Analyze Deep Lifestyle
                    </button>
                </div>
            </form>
"""

# Insert forms before </section>
end_section = content.rfind('</section>')
content = content[:end_section] + new_forms + content[end_section:]

# Update the JS
old_js = """
        function toggleForm(type) {
            document.getElementById('clinical-form').style.display = 'none';
            document.getElementById('cdc-form').style.display = 'none';
            document.getElementById('btn-clinical').classList.remove('active');
            document.getElementById('btn-cdc').classList.remove('active');

            if(type === 'clinical') {
                document.getElementById('clinical-form').style.display = 'grid';
                document.getElementById('btn-clinical').classList.add('active');
            } else {
                document.getElementById('cdc-form').style.display = 'grid';
                document.getElementById('btn-cdc').classList.add('active');
            }
        }
"""

new_js = """
        function toggleForm(type) {
            const forms = ['clinical', 'cdc', 'uci', 'brfss'];
            forms.forEach(f => {
                document.getElementById(f + '-form').style.display = 'none';
                document.getElementById('btn-' + f).classList.remove('active');
            });
            
            document.getElementById(type + '-form').style.display = 'grid';
            document.getElementById('btn-' + type).classList.add('active');
        }
"""

content = content.replace(old_js, new_js)

with open('templates/index.html', 'w') as f:
    f.write(content)
