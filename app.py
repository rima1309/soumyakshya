from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os
import numpy as np
#import scikit-learn
#from scikit-learn.impute import SimpleImputer #Import SimpleImputer class from sklearn.impute

app = Flask(__name__)

# Sample data for dropdowns
options1 = ["Select an Option", "Irrelevant Data", "Duplicate Data", "Missing Data", "Outlier", "Structural Data"]
options2 = {
    "Irrelevant Data": ["Irrelevant Data"],
    "Duplicate Data": ["Duplicate Data"],
    "Missing Data": ["Dropna", "Fillna", "Replace", "Interpolation", "SimpleImputer", "Mean", "Median", "Mode", "List & Pair Deletion", "Prediction Model"],
    "Outlier": ["IQR", "ZScore", "Standard Deviation", "Box Plot"],
    "Structural Data": ["Structural Error"],
}

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to clean the data
def clean_data(data, cleaning_option):
    # Your data cleaning logic goes here
    cleaned_data = data

    if cleaning_option == 'RemoveDuplicates':
        cleaned_data = cleaned_data.drop_duplicates()
    elif cleaning_option == 'RemoveNullValues':
       cleaned_data = cleaned_data.dropna()

    return cleaned_data



@app.route('/')
def index():
    return render_template('index.html', options1=options1)

@app.route('/process', methods=['POST'])
def process():
    selected_option1 = request.form['dropdown1']
    selected_option2 = request.form['dropdown2']

    # Use selected_option2 in different functions
    #result_dropdown = process_data(selected_option2)
    result_dropdown = upload_file(selected_option2)

    #return render_template('result.html', result=result_dropdown)
    return result_dropdown

#def process_data(option):
    # Example function using the selected option
    #return f"You selected option {option}"

#@app.route('/upload', methods=['POST'])
def upload_file(option):
    
    if request.method == 'POST':
        file = request.files['file']
        #cleaning_option = request.form['cleaning_option']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read the CSV file into a pandas DataFrame
            data = pd.read_csv(filepath)
            
            #Clean Duplicate Data
            if option == 'Duplicate Data':
                cleaned_data = data.drop_duplicates()
            
            #Clean Irrelevant Data  
            if option == 'Irrelevant Data':
                cleaned_data = data.drop(["Name","Ticket"],inplace=True,axis=1)
                
            #Clean Missing Data  (Removing Null Values Using dropna)
            if option == 'Dropna':
                cleaned_data = data.dropna()
                
            #Clean Missing Data  (Replace NaN values with any Values Using Fillna)
            if option == 'Fillna':
                cleaned_data = data.fillna(0)
                
            #Clean Missing Data  (Replace NaN values with any constant "0" Using Replace)
            if option == 'Replace':
                cleaned_data = data.replace(np.nan,0)
                
            #Clean Missing Data  (Replace with some intermediate value)
            if option == 'Interpolation':
                
                #cleaned_data = data.interpolate(method='linear', inplace=True)  # --Replace missing values with linear interpolation
                data = data.set_index("Date")
                cleaned_data = data.interpolate(method="time")
                
            #Clean Missing Data  (Missing values can be imputed with a provided constant value)
            #if option == 'SimpleImputer':                
            # we can directly use the fi_transform inplace of fit and then transform
             #   imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
            # Impute NaN value in columns "Day_Temp" with mean value of respected column.
              #  cleaned_data.iloc[:,3:4]=imputer.fit_transform(data.iloc[:,3:4])
                
                
                   
            # Save the cleaned data to a new CSV file
            cleaned_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'cleaned_' + filename)
            
            cleaned_data.to_csv(cleaned_filepath, index=False)
            return render_template('result.html', original_filename=filename, cleaned_filename='cleaned_' + filename)
        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
