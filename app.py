import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import altair as alt
import joblib
import matplotlib.pyplot as plt

from supabase import create_client
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score

SUPABASE_URL = "https://csfaqojfluduffilprnd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzZmFxb2pmbHVkdWZmaWxwcm5kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk1MDAyOTYsImV4cCI6MjA2NTA3NjI5Nn0.kuB-eWHS4EzcegMTAFgwGGgwjfGYBtI3hEv1aTil8UQ"

@st.cache_data
def load_data():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    res = supabase.table("Student").select("*").execute()
    df = pd.DataFrame(res.data)
    return df

def preprocess(df):
    df = df.drop_duplicates()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    y_raw = df['Status']
    le_target = LabelEncoder()
    y = le_target.fit_transform(y_raw)

    X = df.drop("Status", axis=1)
    cat_cols = X.select_dtypes(include='object').columns
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    return X, y, le_target, None

def train_xgb(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    return model, y_test, y_pred, y_prob

def load_model():
    model_bundle = joblib.load('xgboost_model_bundle.pkl')
    model = model_bundle['model']
    le = model_bundle['label_encoder']
    return model, le

def show_dashboard(df):
    st.title("Homepage: Student Dropout Dashboard")

    st.subheader("Distribusi Status Mahasiswa")
    counts = df['Status'].value_counts()
    fig, ax = plt.subplots()
    counts.plot.pie(autopct='%1.1f%%', ax=ax, startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.set_ylabel('')
    st.pyplot(fig)

    gender_map = {0: 'Female', 1: 'Male'}
    df['Gender_Label'] = df['Gender'].map(gender_map)

    st.subheader("Gender Distribution")
    gender_chart = alt.Chart(df).mark_arc().encode(
        theta="count():Q",
        color="Gender_Label:N"
    )
    st.altair_chart(gender_chart, use_container_width=True)

    st.subheader("Admission Grade vs Dropout")
    df['Status_Label'] = df['Status'].apply(lambda x: 'Dropout' if x == 'Dropout' else 'Continue')
    scatter = alt.Chart(df[df['Admission_grade'].notnull()]).mark_circle(size=60).encode(
        x='Admission_grade',
        y=alt.Y('index', title='Student Index'),
        color='Status_Label'
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

    marital_map = {
        1: "Single", 2: "Married", 3: "Widower", 4: "Divorced",
        5: "Facto Union", 6: "Legally Separated"
    }
    df['Marital_Label'] = df['Marital_status'].map(marital_map)
    selected_status = st.selectbox("Select Marital Status", df['Marital_Label'].dropna().unique())
    filtered = df[df['Marital_Label'] == selected_status]
    st.write(filtered[['index', 'Admission_grade', 'Status_Label']])

def show_predict_page(model, le_y, X_cols):
    st.title("Predict Student Dropout")

    input_data = {}

    st.subheader("Masukkan data mahasiswa")

    for col in X_cols.index:
        if X_cols[col].kind == 'f':  # float
            val = st.number_input(f"{col}", format="%.2f")
        elif X_cols[col].kind == 'i':  # integer
            val = st.number_input(f"{col}", step=1, format="%d")
        else:  # kategorikal
            val = st.text_input(f"{col}")
        input_data[col] = val

    if st.button("Predict"):
        input_df = pd.DataFrame([input_data])

        for col in input_df.columns:
            if X_cols[col].kind == 'f':
                input_df[col] = input_df[col].astype(float)
            elif X_cols[col].kind == 'i':
                input_df[col] = input_df[col].astype(int)
            else:
                input_df[col] = input_df[col].astype(str)
                input_df[col] = input_df[col].astype("category").cat.codes

        if 'index' in input_df.columns:
            input_df = input_df.drop(columns=['index'])

        pred_encoded = model.predict(input_df)[0]
        label_map = {
            0: "Enrolled",
            1: "Dropout",
            2: "Graduate"
        }
        pred_label = label_map.get(pred_encoded, "Unknown")

        proba = model.predict_proba(input_df)[0]
        classes = le_y.inverse_transform(range(len(proba)))
        classes = list(label_map.values())
        proba_dict = dict(zip(classes, proba))


        st.success(f"Prediksi: **{pred_label}**")
        st.write("**Probabilitas semua kelas:**")
        for cls, p in proba_dict.items():
            st.write(f"{cls}: {p:.2%}")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Menu", ["Home", "Predict"])

    df = load_data()
    X, y, le, _ = preprocess(df)
    model, le_loaded = load_model()
    X_cols = X.dtypes


    if page == "Home":
        show_dashboard(df)
    elif page == "Predict":
        show_predict_page(model, le_loaded, X_cols)

if __name__ == "__main__":
    main()
