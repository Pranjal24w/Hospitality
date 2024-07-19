# Hospitality
# Hostel Room Allocation System
This Flask application allows users to upload CSV files containing group and hostel information, processes the data to allocate hostel rooms based on group size and gender, and provides a download link for the allocation results.

# Features
File Upload: Users can upload two CSV files: one for group information and one for hostel information.
Data Processing: The application processes the uploaded files to allocate rooms based on group size and gender.
Download Allocation: Users can download the resulting allocation as a CSV file.

# How It Works
1. Flask Application Setup
The Flask application is configured with an upload folder to store uploaded files temporarily:

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

2. Routes
Index Route (/): Displays the upload form.
Upload Route (/upload): Handles file uploads and processes the data.
Download Route (/download): Provides a link to download the allocation results.

# Folder Structure

project-root/
│
├── app.py                 # Flask application
├── templates/
│   └── index.html         # HTML form for file upload
│   └── upload.html        # HTML table to display allocation results
├── uploads/               # Directory to store uploaded files
Running the Application

# Install dependencies:
pip install flask pandas

# Run the application:
python app.py

# Access the application:
Open your web browser and navigate to http://127.0.0.1:5000/.

Troubleshooting
If you encounter a FileNotFoundError, ensure that the uploads directory exists and that the files are being saved correctly. The application will create the directory if it doesn't exist.

# Conclusion
This application provides a simple interface for uploading CSV files, processing data to allocate hostel rooms based on group size and gender, and downloading the results. It uses Flask for the web interface and Pandas for data processing.
