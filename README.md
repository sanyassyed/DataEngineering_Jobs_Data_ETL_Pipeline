### **Job Data Processing and Storage in AWS Cloud**

### **Project Description**  
This mini project involves developing a Python-based data engineering pipeline to extract, transform, and load (ETL) job data from an API into an AWS S3 bucket. The project simulates real-world scenarios of working with APIs, managing cloud resources, and implementing ETL workflows for structured data processing.  

---

### **Scenario**  
The project retrieves job data from the Muse API, focusing on Page 50 of the job listings. The extracted data is transformed into a structured format and stored securely in AWS S3 for further analysis. This project is designed to be deployed and run on an EC2 instance, leveraging both Python and AWS tools for automation and scalability.

---

### **Project Architecture**  
![ProjectArchitecture](./docs/project_jobs.png)

---

### **Technical Details**  
1. **Data Extraction:**  
   - Used Python's `requests` library to query the API at `https://www.themuse.com/api/public/jobs?page=50`.  
   - Extracted fields of interest:  
     - **Company Name**  
     - **Locations**  
     - **Job Name**  
     - **Job Type**  
     - **Publication Date**  

2. **Data Transformation:**  
   - Converted the JSON response to a Pandas DataFrame.  
   - Parsed and cleaned data:  
     - Extracted **city** and **country** from the "locations" field.  
     - Formatted the "publication date" to include only the date.  
   - Renamed columns for clarity:  
     - `company.name` → `company_name`  
     - `name` → `job_name`  
     - `type` → `job_type`  
     - `publication_date` → `date`  

3. **Data Storage:**  
   - Saved the transformed data as a Parquet file for efficient storage and retrieval.  
   - Used **AWS S3** for data storage:  
     - [X]Option 1: Used `boto3` with AWS credentials to programmatically upload the file.  
     - []Option 2: Configure IAM roles for the EC2 instance and use AWS CLI (`aws s3 cp`) to upload the file.  

4. **Automation:**  
   - Created a shell script to initialize the project environment, set up virtual environments, and run the Python script.  
   - Used configuration files (e.g., `.env` for secrets, `.toml` for parameters) to decouple settings from the code.  

5. **Environment Setup:**  
   - Deployed the project on an AWS EC2 instance.  
   - Used VSCode for remote SSH access to EC2 for code development and debugging.

6. **Server Used:**
   - `MiniProject`: a t2.micro EC2 instance
---

### **Tools Used**
- Python
   - Pandas
   - Boto3
   - Numpy
   - Requests
- AWS EC2
- AWS S3
- Shell
- VSCode

---

### **Project Structure**  
- **`.v_env`**: Python virtual environment.  
- **`requirements.txt`**: Contains the dependency packages required for this project.  
- **`config.toml`**: Contains API and AWS parameters for configuring the project.  
- **`.env`**: Contains API and AWS secrets.  
- **`script/init.sh`**: Shell script to initiate the project by creating
   - Installing Python
   - Creating virtual env
   - Installing packages listed in requirements.txt to the virtual env
- **`script/run.py`**: Python ETL script for extracting, transforming, and loading the data.  
- **`script/run.sh`**: Shell script to control the execution of:  
   - Set environment variables  
   - Run the Python script (in either test mode or production mode).  
- **`script/read.py`**: Python script used for testing to read the parquet file from s3 and write into local system as csv.
   - Run this file as `python3 script/read.py`
   - Add the file name to be downloaded in config.toml at `['aws']['file_name']`
   - The file will be downloaded at `output/output.csv`
- **`logs/`**: Contains log files for debugging and auditing.  
- **`.gitignore`**: Specifies files to ignore in version control.

---

### **Project Setup**

```bash
git clone https://github.com/sanyassyed/DataEngineering_Jobs_Data_ETL_Pipeline.git
cd DataEngineering_Jobs_Data_ETL_Pipeline
bash ./script/init.sh
# Add the secrets to env_blueprint
# api key and access key and secret key to access s3 bucket
nano env_boilerplate
# rename env_boilerplate to .env
mv env_boilerplate .env
```
---

### **Running the project**
Run the project as follows: NOTE:default mode is production mode; to run in test mode change the code in [run.sh](./script/run.sh):  

```bash
# This will run the project in production mode
bash ./script/run.sh
```

---

### **Testing**
To read back the data written to the s3 bucket do the following:
- Under [aws] in `config.toml` update the file name.
- Then run the read script as follows:
   ```bash
   source ./.v_env_bin/activate
   python3 ./script/read.py
   ```
- The output file `output.csv` will then be available in the [output](./output/) folder
- This helps you check the data written to s3

---

### **Resources**  
- [API Documentation](https://muse.ai/api#flow)
