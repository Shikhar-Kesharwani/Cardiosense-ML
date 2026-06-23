import os

with open('templates/index.html', 'r') as f:
    content = f.read()

# Replace the UCI button with NHANES button
content = content.replace("id=\"btn-uci\" class=\"toggle-btn\" onclick=\"toggleForm('uci')\"", "id=\"btn-nhanes\" class=\"toggle-btn\" onclick=\"toggleForm('nhanes')\"")

# Find the start and end of the uci form
start_form = content.find('<!-- UCI FORM -->')
end_form = content.find('</form>', start_form) + 7

with open('nhanes_form.html', 'r') as f:
    nhanes_content = f.read()

new_form = f"""<!-- NHANES FORM -->
            <form action="/predict_nhanes" method="post" class="grid-form" id="nhanes-form" style="display: none;">
                {nhanes_content}
                <div class="form-actions full-width">
                    <button type="submit" class="glow-button">
                        <i class="fa-solid fa-microchip"></i> Analyze NHANES Data
                    </button>
                </div>
            </form>"""

content = content[:start_form] + new_form + content[end_form:]

# Update the JS array from uci to nhanes
content = content.replace("['clinical', 'cdc', 'uci', 'brfss']", "['clinical', 'cdc', 'nhanes', 'brfss']")

with open('templates/index.html', 'w') as f:
    f.write(content)
print("Updated index.html")
