import os
import json

# file paths
HTML_FILE = 'templates/index.html'
JS_FUNCTIONS_FILE = 'static/js/analysisCallFunctions.js'
JS_FILE = '/static/js/script.js'
APP_FILE = 'app.py'
PLOTTING_FILE = 'plotting.py'
CONFIG_FILE = 'config.json'
ANALYSIS_OPTIONS_FILE = 'analysis_options.json'

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    return config

def load_analysis_options():
    if os.path.exists(ANALYSIS_OPTIONS_FILE):
        with open(ANALYSIS_OPTIONS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_analysis_options(analysis_options):
    with open(ANALYSIS_OPTIONS_FILE, 'w') as file:
        json.dump(analysis_options, file, indent=4)

def add_button_to_html(process_name, process_title):
    button_html = f'            <button onclick="get_{process_name.capitalize()}()">{process_title}</button>\n'
    
    with open(HTML_FILE, 'r') as file:
        lines = file.readlines()
    
    div_found = False
    with open(HTML_FILE, 'w') as file:
        for line in lines:
            file.write(line)
            if '<div id="plot-options" style="display: none">' in line and not div_found:
                file.write(button_html)
                div_found = True
                
    if not div_found:
        print(f"Error: <div id='plot-options' style='display: none;'> not found in {HTML_FILE}")
    else:
        print(f'Added button for {process_name} to {HTML_FILE}')

def add_function_to_js(process_name, process_title):
    function_name = f"get_{process_name.capitalize()}"
    function_js = f"""
function {function_name}() {{
    generatePlot('{process_name}', '{process_title}');
}}\n"""

    with open(JS_FUNCTIONS_FILE, 'r') as file:
        content = file.read()
    
    if function_name not in content:
        with open(JS_FUNCTIONS_FILE, 'a') as file:
            file.write(function_js)
        print(f'Added function for {process_name} to {JS_FUNCTIONS_FILE}')
    else:
        print(f'Function {function_name} already exists in {JS_FUNCTIONS_FILE}')

def add_option_to_plot_route(process_name):
    plot_option = f"        elif plot_type == '{process_name}':\n            plot_{process_name}(df, output_file)\n"
    
    with open(APP_FILE, 'r') as file:
        lines = file.readlines()
        
    import_line_index = -1
    for i, line in enumerate(lines):
        if line.startswith('from plotting import'):
            import_line_index = i
            break
    
    if import_line_index == -1:
        print(f"Error: 'from plotting import' line not found in {APP_FILE}")
        return
    
    import_line = lines[import_line_index].strip()
    if f'plot_{process_name}' not in import_line:
        new_import_line = import_line + f', plot_{process_name}'
        lines[import_line_index] = new_import_line + '\n'
        
    else_line_index = -1
    for i, line in enumerate(lines):
        if line.strip() == 'else:':
            else_line_index = i
            break
    
    if else_line_index == -1:
        print(f"Error: 'else:' line not found in {APP_FILE}")
        return

    lines.insert(else_line_index, plot_option)
    
    with open(APP_FILE, 'w') as file:
        file.writelines(lines)
    
    print(f'Added option for {process_name} to {APP_FILE}')

def add_placeholder_function_to_plotting(process_name):
    function_name = f'plot_{process_name}'
    function_def = f'def {function_name}(df, output_file):\n'
    placeholder_content = f"""    # ---------- place holder for {process_name} logic ----------
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, 'Logic Not Implemented', horizontalalignment='center', verticalalignment='center', fontsize=20, color='red')
    plt.gca().set_facecolor('black')
    plt.gcf().patch.set_facecolor('black')
    plt.axis('off')
    plt.savefig(output_file)
    print(f'Plot saved to {{output_file}} with placeholder content')\n"""
    
    function_code = function_def + placeholder_content
    
    with open(PLOTTING_FILE, 'r') as file:
        content = file.read()
    
    if function_name not in content:
        if '__name__' in content:
            main_index = content.index('if __name__ == "__main__":')
            content = content[:main_index] + '\n' + function_code + '\n' + content[main_index:]
        else:
            content += '\n' + function_code

        with open(PLOTTING_FILE, 'w') as file:
            file.write(content)
        print(f'Added placeholder function for {process_name} to {PLOTTING_FILE}')
    else:
        print(f'Function {function_name} already exists in {PLOTTING_FILE}')

def ensure_data_processing_logic(process_name, process_title):
    add_button_to_html(process_name, process_title)
    add_function_to_js(process_name, process_title)
    add_option_to_plot_route(process_name)
    add_placeholder_function_to_plotting(process_name)
    print(f'Successfully ensured data processing logic for {process_name}')

if __name__ == '__main__':
    config = load_config()
    analysis_options = load_analysis_options()
    for option in config['processing_options']:
        if option['name'] not in analysis_options:
            ensure_data_processing_logic(option['name'], option['title'])
            analysis_options.append(option['name'])
    save_analysis_options(analysis_options)
    print("Build process completed successfully")