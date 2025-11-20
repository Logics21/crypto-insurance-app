import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="SigmaShield | Decentralized Insurance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for DeFi-style design (similar to SigmaFi)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .defi-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 20px 30px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-text {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Stats Cards */
    .stats-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .stat-value {
        color: #f1f5f9;
        font-size: 24px;
        font-weight: 700;
    }
    
    .stat-value-small {
        color: #f1f5f9;
        font-size: 16px;
        font-weight: 600;
    }
    
    /* Pool Cards */
    .pool-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .pool-card:hover {
        border-color: rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
    }
    
    .pool-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .pool-title {
        color: #f1f5f9;
        font-size: 18px;
        font-weight: 600;
    }
    
    .badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-active {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .badge-inactive {
        background: rgba(148, 163, 184, 0.2);
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    /* Risk Badges */
    .risk-low {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .risk-medium {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    .risk-high {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    /* Info Grid */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    
    .info-item {
        display: flex;
        justify-content: space-between;
        padding: 12px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    .info-label {
        color: #94a3b8;
        font-size: 14px;
    }
    
    .info-value {
        color: #f1f5f9;
        font-size: 14px;
        font-weight: 600;
    }
    
    /* Connect Wallet Button */
    .connect-wallet-btn {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .connect-wallet-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }
    
    /* Payout Display */
    .payout-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }
    
    .payout-label {
        color: #86efac;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .payout-value {
        color: #22c55e;
        font-size: 32px;
        font-weight: 700;
    }
    
    .payout-roi {
        color: #86efac;
        font-size: 16px;
        margin-top: 8px;
    }
    
    /* Section Headers */
    .section-header {
        color: #f1f5f9;
        font-size: 24px;
        font-weight: 700;
        margin: 30px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Streamlit overrides */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #f1f5f9;
        border-radius: 8px;
    }
    
    .stSlider > div > div > div {
        background: rgba(99, 102, 241, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Mock insurance pools data
MOCK_POOLS = [
    {
        "id": 1,
        "name": "ETH Price Protection",
        "coverage_amount": 1000,
        "insurance_type": "variable",
        "payout_ratio": 2.0,
        "pool_size": 2000,
        "duration_days": 30,
        "status": "active",
        "tvl": 2000,
        "filled": 100,
        "active": True  # Only this one works
    },
    {
        "id": 2,
        "name": "BTC Volatility Shield",
        "coverage_amount": 5000,
        "insurance_type": "variable",
        "payout_ratio": 3.0,
        "pool_size": 15000,
        "duration_days": 60,
        "status": "active",
        "tvl": 12000,
        "filled": 80,
        "active": False
    },
    {
        "id": 3,
        "name": "Stablecoin Depeg Insurance",
        "coverage_amount": 2500,
        "insurance_type": "fixed",
        "payout_ratio": 1.0,
        "pool_size": 5000,
        "duration_days": 90,
        "status": "active",
        "tvl": 5000,
        "filled": 100,
        "active": False
    },
    {
        "id": 4,
        "name": "Smart Contract Risk Cover",
        "coverage_amount": 3000,
        "insurance_type": "variable",
        "payout_ratio": 2.5,
        "pool_size": 9000,
        "duration_days": 45,
        "status": "pending",
        "tvl": 3500,
        "filled": 39,
        "active": False
    }
]

def calculate_payouts(coverage_amount, insurance_type, payout_ratio, pool_size, my_stake):
    """
    Calculate payouts using the EXACT original logic
    """
    if insurance_type != "fixed":
        # Variable insurance - EXACT original logic
        insurer_max_payout = pool_size * (1 / payout_ratio)
        buyer_max_payout = coverage_amount * payout_ratio
        
        insurer_actual_payout = min(insurer_max_payout, coverage_amount)
        buyer_actual_payout = min(buyer_max_payout, pool_size)
        
        my_earnings = (my_stake / pool_size) * insurer_actual_payout
    else:
        # Fixed insurance
        insurer_actual_payout = coverage_amount
        buyer_actual_payout = pool_size
        my_earnings = (my_stake / pool_size) * insurer_actual_payout
    
    return {
        'insurer_payout': insurer_actual_payout,
        'buyer_payout': buyer_actual_payout,
        'my_earnings': my_earnings,
        'pool_share': (my_stake / pool_size) * 100
    }

def calculate_roi(payout, investment):
    """Calculate ROI percentage"""
    return ((payout - investment) / investment * 100) if investment > 0 else 0

# Initialize session state
if 'selected_pool' not in st.session_state:
    st.session_state.selected_pool = None

# Header
st.markdown("""
    <div class="defi-header">
        <div class="logo-section">
            <div class="logo-text">🛡️ SigmaShield</div>
            <div style="color: #94a3b8; font-size: 14px;">Decentralized Insurance Protocol</div>
        </div>
        <div>
            <button class="connect-wallet-btn">Connect Wallet</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Stats Overview
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stats-card">
            <div class="stat-label">Total Value Locked</div>
            <div class="stat-value">$22.5M</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stats-card">
            <div class="stat-label">Active Pools</div>
            <div class="stat-value">24</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stats-card">
            <div class="stat-label">Coverage Provided</div>
            <div class="stat-value">$8.3M</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stats-card">
            <div class="stat-label">Avg APY</div>
            <div class="stat-value">12.4%</div>
        </div>
        """, unsafe_allow_html=True)

# Main tabs
tab1, tab2 = st.tabs(["🏪 Insurance Marketplace", "💼 My Positions"])

with tab1:
    st.markdown('<div class="section-header">Available Insurance Pools</div>', unsafe_allow_html=True)
    
    # Display pools in a grid
    cols = st.columns(2)
    
    for idx, pool in enumerate(MOCK_POOLS):
        with cols[idx % 2]:
            # Determine risk level
            if pool['payout_ratio'] < 2.0:
                risk_class = "risk-low"
                risk_text = "LOW RISK"
            elif pool['payout_ratio'] < 3.0:
                risk_class = "risk-medium"
                risk_text = "MEDIUM RISK"
            else:
                risk_class = "risk-high"
                risk_text = "HIGH RISK"
            
            status_badge = "badge-active" if pool['status'] == "active" else "badge-inactive"
            status_text = pool['status'].upper()
            
            st.markdown(f"""
                <div class="pool-card">
                    <div class="pool-header">
                        <div class="pool-title">{pool['name']}</div>
                        <span class="badge {status_badge}">{status_text}</span>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">Coverage</span>
                            <span class="info-value">${pool['coverage_amount']:,}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Pool Size</span>
                            <span class="info-value">${pool['pool_size']:,}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Type</span>
                            <span class="info-value">{pool['insurance_type'].capitalize()}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Ratio</span>
                            <span class="info-value">{pool['payout_ratio']:.1f}:1</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Duration</span>
                            <span class="info-value">{pool['duration_days']} days</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Risk</span>
                            <span class="badge {risk_class}" style="padding: 4px 8px; font-size: 10px;">{risk_text}</span>
                        </div>
                    </div>
                    <div style="margin-top: 16px;">
                        <div style="color: #94a3b8; font-size: 12px; margin-bottom: 8px;">Pool Filled: {pool['filled']}%</div>
                        <div style="background: rgba(15, 23, 42, 0.8); border-radius: 8px; height: 8px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%); width: {pool['filled']}%; height: 100%;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Only the first pool is functional
            if pool['active']:
                if st.button(f"View Details →", key=f"view_{pool['id']}", use_container_width=True):
                    st.session_state.selected_pool = pool
                    st.rerun()
            else:
                st.button(f"Coming Soon", key=f"view_{pool['id']}", use_container_width=True, disabled=True)

# Pool Details Modal/Section
if st.session_state.selected_pool:
    st.markdown("---")
    pool = st.session_state.selected_pool
    
    st.markdown(f'<div class="section-header">📊 {pool["name"]} - Pool Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔒 Buy Insurance")
        
        st.markdown(f"""
            <div class="pool-card">
                <div style="margin-bottom: 16px;">
                    <div class="stat-label">Coverage Amount</div>
                    <div class="stat-value-small">${pool['coverage_amount']:,} USDC</div>
                </div>
                <div style="margin-bottom: 16px;">
                    <div class="stat-label">Insurance Type</div>
                    <div class="stat-value-small">{pool['insurance_type'].capitalize()}</div>
                </div>
                <div style="margin-bottom: 16px;">
                    <div class="stat-label">Payout Ratio</div>
                    <div class="stat-value-small">{pool['payout_ratio']:.1f}:1</div>
                </div>
                <div>
                    <div class="stat-label">Duration</div>
                    <div class="stat-value-small">{pool['duration_days']} days</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Calculate buyer payout
        payouts = calculate_payouts(
            pool['coverage_amount'],
            pool['insurance_type'],
            pool['payout_ratio'],
            pool['pool_size'],
            pool['pool_size'] / 2  # Default stake
        )
        
        buyer_roi = calculate_roi(payouts['buyer_payout'], pool['coverage_amount'])
        
        st.markdown(f"""
            <div class="payout-box">
                <div class="payout-label">💎 Your Potential Payout (if claim)</div>
                <div class="payout-value">${payouts['buyer_payout']:,.2f}</div>
                <div class="payout-roi">ROI: +{buyer_roi:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="pool-card">
                <div style="color: #94a3b8; font-size: 14px; margin-bottom: 12px;">📌 How it works:</div>
                <div style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">
                    • Lock <strong>${pool['coverage_amount']:,} USDC</strong> as premium<br>
                    • If claim triggers: Get <strong>${payouts['buyer_payout']:,.2f} USDC</strong><br>
                    • If no claim: Insurers keep your premium<br>
                    • Funds locked for <strong>{pool['duration_days']} days</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔐 Lock Funds & Buy Insurance", use_container_width=True):
            st.success("✅ Insurance purchased successfully!")
            st.balloons()
    
    with col2:
        st.markdown("### 📈 Provide Coverage")
        
        st.markdown("#### Pool Configuration")
        my_stake = st.number_input(
            "Your Stake (USDC)",
            min_value=100,
            max_value=pool['pool_size'],
            value=1000,
            step=100,
            help="Your contribution to the insurance pool"
        )
        
        # Calculate with updated stake
        payouts = calculate_payouts(
            pool['coverage_amount'],
            pool['insurance_type'],
            pool['payout_ratio'],
            pool['pool_size'],
            my_stake
        )
        
        my_roi = calculate_roi(payouts['my_earnings'], my_stake)
        
        st.markdown(f"""
            <div class="pool-card">
                <div style="margin-bottom: 16px;">
                    <div class="stat-label">Your Pool Share</div>
                    <div class="stat-value-small">{payouts['pool_share']:.2f}%</div>
                    <div style="margin-top: 8px; background: rgba(15, 23, 42, 0.8); border-radius: 8px; height: 8px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #06b6d4 0%, #22c55e 100%); width: {payouts['pool_share']}%; height: 100%;"></div>
                    </div>
                </div>
                <div>
                    <div class="stat-label">Total Pool Size</div>
                    <div class="stat-value-small">${pool['pool_size']:,} USDC</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="payout-box">
                <div class="payout-label">💰 Your Earnings (if no claim)</div>
                <div class="payout-value">${payouts['my_earnings']:,.2f}</div>
                <div class="payout-roi">ROI: {'+' if my_roi > 0 else ''}{my_roi:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="pool-card">
                <div style="color: #94a3b8; font-size: 14px; margin-bottom: 12px;">📌 How it works:</div>
                <div style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">
                    • Stake <strong>${my_stake:,} USDC</strong> to the pool<br>
                    • If no claim: Earn <strong>${payouts['my_earnings']:,.2f} USDC</strong><br>
                    • If claim triggers: Pay <strong>${(my_stake - payouts['my_earnings']):,.2f} USDC</strong><br>
                    • Your share: <strong>{payouts['pool_share']:.2f}%</strong> of pool
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("💼 Provide Coverage", use_container_width=True):
            st.success("✅ Coverage provided successfully!")
            st.balloons()
    
    # Close button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Marketplace", use_container_width=True):
        st.session_state.selected_pool = None
        st.rerun()

with tab2:
    st.markdown('<div class="section-header">My Active Positions</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="pool-card" style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
            <div style="color: #94a3b8; font-size: 18px; margin-bottom: 8px;">No active positions</div>
            <div style="color: #64748b; font-size: 14px;">Connect your wallet and participate in insurance pools</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
        SigmaShield Protocol • Powered by Smart Contracts • Audited by CertiK
    </div>
    """, unsafe_allow_html=True)
