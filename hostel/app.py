from flask import Flask, request, render_template, redirect, url_for,send_file
import os 
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'group_file' not in request.files or 'hostel_file' not in request.files:
        return redirect(request.url)
    
    group_file = request.files['group_file']
    hostel_file = request.files['hostel_file']
    
    if group_file.filename == '' or hostel_file.filename == '':
        return redirect(request.url)
    
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    group_path = os.path.join(app.config['UPLOAD_FOLDER'], group_file.filename)
    hostel_path = os.path.join(app.config['UPLOAD_FOLDER'], hostel_file.filename)
    
    group_file.save(group_path)
    hostel_file.save(hostel_path)
    
    group_df = pd.read_csv(group_path)
    hostel_df = pd.read_csv(hostel_path)
    
    allocation = allocate_rooms(group_df, hostel_df)
    allocation_path = os.path.join(app.config['UPLOAD_FOLDER'], 'allocation.csv')
    
    # Debugging: Print statements to verify the paths and DataFrames
    print(f"Group file saved to: {group_path}")
    print(f"Hostel file saved to: {hostel_path}")
    print(f"Allocation file will be saved to: {allocation_path}")
    
    allocation.to_csv(allocation_path, index=False)
    
    # Verify that the file has been created
    if os.path.exists(allocation_path):
        print(f"File created successfully: {allocation_path}")
    else:
        print(f"Failed to create file: {allocation_path}")
    
    
    return render_template('upload.html', tables=[allocation.to_html(classes='data', header="true")])

def allocate_rooms(group_df, hostel_df):
    allocation = []

    # Loop through each group
    for _, group in group_df.iterrows():
        group_id = group['Group ID']
        members = group['Members']
        gender = group['Gender']

        # Filter hostels based on gender
        suitable_hostels = hostel_df[hostel_df['Gender'].str.contains(gender.split()[0])]

        for _, hostel in suitable_hostels.iterrows():
            if hostel['Capacity'] >= members:
                allocation.append({
                    'Group ID': group_id,
                    'Hostel Name': hostel['Hostel Name'],
                    'Room Number': hostel['Room Number'],
                    'Members Allocated': members
                })
                hostel['Capacity'] -= members
                break

    allocation_df = pd.DataFrame(allocation)
    return allocation_df

@app.route('/download')
def download():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'allocation.csv')
    # Check if the file exists before attempting to send it
    if os.path.exists(path):
        print(f"File found for download: {path}")
        return send_file(path, as_attachment=True)
    else:
        print(f"File not found for download: {path}")
        return "File not found", 404

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
