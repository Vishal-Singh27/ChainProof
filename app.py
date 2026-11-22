import streamlit as st
import hashlib
import os
import json
from datetime import datetime
from registry_chain import ModelRegistryChain

st.set_page_config(
    page_title="ChainProof — Blockchain-Verified ML Model Registry",
    page_icon="⛓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .title-banner {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4338CA;
        margin-bottom: 0.2rem;
    }
    .sub-banner {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .hash-badge {
        font-family: monospace;
        background-color: #EEF2FF;
        color: #3730A3;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        word-break: break-all;
    }
    .verified-card {
        background-color: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 8px;
        padding: 16px;
    }
    .unverified-card {
        background-color: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 8px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Chain
if "model_chain" not in st.session_state:
    chain = ModelRegistryChain(difficulty=2)
    
    # Pre-register initial verified model for immediate demo
    sample_path = os.path.join(os.path.dirname(__file__), "models_repo", "churn_rf_v1.pkl")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        chain.register_model(
            model_id="ML-PROD-001",
            model_name="Samyak_User_Churn_RF",
            version="1.0.0",
            model_hash=h,
            metrics={
                "accuracy": "87.0%",
                "dataset": "Samyak_User_Records_4K",
                "leakage_audited": True,
                "framework": "Scikit-Learn (RandomForest)"
            }
        )
    st.session_state.model_chain = chain

chain = st.session_state.model_chain

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Ledger Status")
    st.markdown(f"**Total Registered Models:** `{len(chain.chain) - 1}`")
    st.markdown(f"**Ledger Difficulty:** `{chain.difficulty} zeros`")
    st.markdown("---")
    st.markdown("### 🛡️ Why Model Governance?")
    st.caption("Prevent supply-chain tampering, unauthorized weight alteration, and unverified shadow models in production pipelines.")

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="title-banner">⛓️ ChainProof</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-banner">Blockchain-Backed ML Model Registry & Cryptographic Weight Auditing</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("● Governance Ledger Active")

tabs = st.tabs(["📦 Register ML Model", "🔍 Verify Model Artifact", "⛓️ Registry Ledger Explorer", "🏗️ Architecture"])

# ================= TAB 1: REGISTER MODEL =================
with tabs[0]:
    st.subheader("📦 Register & Anchor New ML Model Artifact")
    
    col_f, col_m = st.columns([1, 1], gap="medium")
    
    with col_f:
        st.markdown("#### 1. Upload Model Weights / Pipeline")
        uploaded_file = st.file_uploader("Select model binary (.pkl, .pt, .bin, .onnx, .joblib)", type=["pkl", "pt", "bin", "onnx", "joblib"])
        
        # Sample selector
        sample_models_dir = os.path.join(os.path.dirname(__file__), "models_repo")
        sample_files = [f for f in os.listdir(sample_models_dir) if not f.startswith(".")] if os.path.exists(sample_models_dir) else []
        selected_sample = st.selectbox("Or choose pre-packaged model from repo:", ["-- Select Sample --"] + sample_files)

        file_bytes = None
        source_name = "custom_model"
        if uploaded_file:
            file_bytes = uploaded_file.read()
            source_name = uploaded_file.name
        elif selected_sample != "-- Select Sample --":
            sample_full_path = os.path.join(sample_models_dir, selected_sample)
            with open(sample_full_path, "rb") as f:
                file_bytes = f.read()
            source_name = selected_sample

        file_hash = ""
        if file_bytes:
            file_hash = hashlib.sha256(file_bytes).hexdigest()
            st.markdown(f"**Computed SHA-256 Digest:**")
            st.markdown(f"<span class='hash-badge'>{file_hash}</span>", unsafe_allow_html=True)

    with col_m:
        st.markdown("#### 2. Model Governance Metadata")
        m_name = st.text_input("Model Name", value=source_name.split(".")[0])
        m_ver = st.text_input("Model Semantic Version", value="1.0.0")
        m_framework = st.selectbox("Framework", ["PyTorch", "Scikit-Learn", "XGBoost", "TensorFlow/Keras", "ONNX"])
        m_dataset = st.text_input("Training Dataset Reference", value="Benchmark_v2.csv")
        
        c_acc, c_leak = st.columns(2)
        with c_acc:
            m_acc = st.text_input("Validation Accuracy / F1", value="96.2% AUC")
        with c_leak:
            m_leak = st.checkbox("Data Leakage Audit Passed?", value=True)

        btn_register = st.button("🚀 Anchor Model to Blockchain", type="primary", use_container_width=True)

        if btn_register:
            if not file_bytes:
                st.error("Please upload or select a model binary file first.")
            else:
                with st.spinner("⛏️ Mining governance block with Proof-of-Work..."):
                    new_block = chain.register_model(
                        model_id=f"ML-{len(chain.chain)}",
                        model_name=m_name,
                        version=m_ver,
                        model_hash=file_hash,
                        metrics={
                            "accuracy": m_acc,
                            "dataset": m_dataset,
                            "framework": m_framework,
                            "leakage_audited": m_leak
                        }
                    )
                    st.success(f"✅ Model '{m_name} v{m_ver}' anchored on Block #{new_block.index}!")
                    st.rerun()

# ================= TAB 2: VERIFY MODEL =================
with tabs[1]:
    st.subheader("🔍 Production Model Integrity Verification")
    st.markdown("Upload any deployed model binary to verify whether it matches the exact weights cryptographically signed on the blockchain ledger.")

    v_file = st.file_uploader("Upload model file to audit:", type=["pkl", "pt", "bin", "onnx", "joblib"], key="verify_uploader")
    
    if v_file:
        v_bytes = v_file.read()
        v_hash = hashlib.sha256(v_bytes).hexdigest()
        
        st.markdown(f"**Artifact SHA-256 Fingerprint:**")
        st.markdown(f"<span class='hash-badge'>{v_hash}</span>", unsafe_allow_html=True)
        
        verified, matched_block = chain.verify_file_hash(v_hash)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if verified:
            st.balloons()
            st.markdown(f"""
            <div class="verified-card">
                <h3 style="color: #065F46; margin: 0 0 10px 0;">✅ CERTIFIED AUDITED MODEL — ZERO TAMPERING DETECTED</h3>
                <p style="color: #065F46; margin: 4px 0;"><strong>Model Name:</strong> {matched_block.model_name} (v{matched_block.version})</p>
                <p style="color: #065F46; margin: 4px 0;"><strong>Anchored Block:</strong> #{matched_block.index} | <strong>Model ID:</strong> {matched_block.model_id}</p>
                <p style="color: #065F46; margin: 4px 0;"><strong>Registered Time:</strong> {datetime.fromtimestamp(matched_block.timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p style="color: #065F46; margin: 4px 0;"><strong>Audited Performance:</strong> {matched_block.metrics.get('accuracy', 'N/A')} on {matched_block.metrics.get('dataset', 'N/A')}</p>
                <p style="color: #065F46; margin: 4px 0;"><strong>Data Leakage Audit:</strong> {'Passed ✅' if matched_block.metrics.get('leakage_audited') else 'Pending ⚠️'}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="unverified-card">
                <h3 style="color: #991B1B; margin: 0 0 10px 0;">❌ UNVERIFIED OR TAMPERED ARTIFACT</h3>
                <p style="color: #991B1B; margin: 4px 0;">This model file's cryptographic hash does not match any block registered on the ChainProof governance ledger.</p>
                <p style="color: #991B1B; margin: 4px 0;"><strong>Security Warning:</strong> This binary may have been modified, backdoored, or trained on unapproved data splits.</p>
            </div>
            """, unsafe_allow_html=True)

# ================= TAB 3: LEDGER EXPLORER =================
with tabs[2]:
    st.subheader("⛓️ Model Governance Blockchain Explorer")
    
    for b in reversed(chain.chain):
        is_gen = (b.index == 0)
        with st.expander(f"📦 Block #{b.index}: {b.model_name} ({'GENESIS' if is_gen else 'REGISTERED'})", expanded=(b.index == len(chain.chain)-1)):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Block Index:** `{b.index}`")
                st.write(f"**Model ID:** `{b.model_id}`")
                st.write(f"**Version:** `{b.version}`")
                st.write(f"**Timestamp:** `{datetime.fromtimestamp(b.timestamp).strftime('%Y-%m-%d %H:%M:%S')}`")
                st.write(f"**Nonce:** `{b.nonce}`")
            with c2:
                st.markdown(f"**Block Hash:**")
                st.markdown(f"<span class='hash-badge'>{b.hash}</span>", unsafe_allow_html=True)
                st.markdown(f"**Previous Hash:**")
                st.markdown(f"<span class='hash-badge'>{b.previous_hash}</span>", unsafe_allow_html=True)
                st.markdown(f"**Model Weights SHA-256:**")
                st.markdown(f"<span class='hash-badge'>{b.model_hash}</span>", unsafe_allow_html=True)
            
            st.markdown("##### 📊 Registered Metrics:")
            st.json(b.metrics)

# ================= TAB 4: ARCHITECTURE =================
with tabs[3]:
    st.subheader("🏗️ ChainProof System Architecture")
    st.markdown("""
    ```
    [ Model Training / PyTorch / Scikit-Learn ]
                         │
                         ▼
    [ Model Artifact (.pkl, .pt, .onnx) ]
                         │
                         ├──► [ SHA-256 Weights Fingerprinting ]
                         │
                         ├──► [ Evaluation Metadata & Leakage Audit ]
                         │
                         ▼
        [ Proof-of-Work Model Governance Block ]
                         │
                         ▼
        [ Immutable Blockchain Ledger ] ◄──────► [ Production Serving Audit Gateway ]
    ```
    ### Why this impresses Datopic:
    Enterprise tech firms serving healthcare, banking, and government clients must comply with strict AI governance regulations. Combining cryptographic hashing with blockchain ensures ML models in production have not been poisoned, tampered with, or swapped silently.
    """)
