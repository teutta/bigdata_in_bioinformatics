import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle
# Molecular descriptor calculator
def desc_calc():
    # Performs the descriptor calculation
    # Read in calculated descriptors and display the dataframe
    st.subheader('Calculated molecular descriptors')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.markdown(filedownload(desc), unsafe_allow_html=True)
    # Write the data dimension (number of molecules and descriptors)
    nmol = desc.shape[0]
    ndesc = desc.shape[1]
    st.info('Selected fingerprint: ' + user_fp)
    st.info('Number of molecules: ' + str(nmol))
    st.info('Number of descriptors: ' + str(ndesc-1))
    os.remove('molecule.smi')
    
# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="descriptor_{user_fp}.csv">Download CSV File</a>'
    return href

# Page title
st.markdown("""
## BIOINFROMATICS PREDICTION 
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])


with st.sidebar.header('2. Enter column names '):
    name_mol = st.sidebar.text_input('Enter column name for Molecule ID', 'molecule_chembl_id')
    name_smiles = st.sidebar.text_input('Enter column name for SMILES', 'canonical_smiles')


with st.sidebar.header('3. Set parameters'):
    # Select fingerprint
    fp_dict = {'AtomPairs2D':'AtomPairs2DFingerprinter.xml',
               'AtomPairs2DCount':'AtomPairs2DFingerprintCount.xml',
               'CDK':'Fingerprinter.xml',
               'CDKextended':'ExtendedFingerprinter.xml',
               'CDKgraphonly':'GraphOnlyFingerprinter.xml',
               'EState':'EStateFingerprinter.xml',
               'KlekotaRoth':'KlekotaRothFingerprinter.xml',
               'KlekotaRothCount':'KlekotaRothFingerprintCount.xml',
               'MACCS':'MACCSFingerprinter.xml',
               'PubChem':'PubchemFingerprinter.xml',
               'Substructure':'SubstructureFingerprinter.xml',
               'SubstructureCount':'SubstructureFingerprintCount.xml'}
    user_fp = st.sidebar.selectbox('Choose fingerprint to calculate', list(fp_dict.keys()) )
    selected_fp = fp_dict[user_fp]

    # Set number of molecules to compute
    df0 = pd.read_csv('acetylcholinesterase_04_bioactivity_data_3class_pIC50.csv')
    all_mol = df0.shape[0]
    number2calc = st.sidebar.slider('How many molecules to compute?', min_value=10, max_value=all_mol, value=10, step=10)


if uploaded_file is not None:
    # Read CSV data
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file).iloc[:number2calc,1:]
        return csv
    df = load_csv()
    df2 = pd.concat([df[name_smiles], df[name_mol]], axis=1)
    # Write CSV data
    df2.to_csv('molecule.smi', sep = '\t', header = False, index = False)
    st.subheader('Initial data from CSV file')
    st.write(df)
    st.subheader('Formatted as PADEL input file')
    st.write(df2)
    with st.spinner("Calculating descriptors..."):
        desc_calc()
        
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Read CSV data
        @st.cache
        def load_data():
            # number2calc specifies the number of molecules to compute
            df = pd.read_csv('acetylcholinesterase_04_bioactivity_data_3class_pIC50.csv').iloc[:number2calc,1:]
            return df
        df = load_data()
        df2 = pd.concat([df[name_smiles], df[name_mol]], axis=1)
        # Write CSV data
        df2.to_csv('molecule.smi', sep = '\t', header = False, index = False)
        st.subheader('Initial data from CSV file')
        st.write(df)
        st.subheader('Formatted as PADEL input file')
        st.write(df2)
        with st.spinner("Calculating descriptors..."):
            desc_calc()
