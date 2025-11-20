import streamlit as st
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="SigmaShield | Insurance Marketplace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for SigmaFi-style design
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: #e8eaed;
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }
    
    /* Header */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 30px;
        background: white;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .tvl-display {
        color: #666;
        font-size: 14px;
    }
    
    .tvl-value {
        color: #1a1a1a;
        font-weight: 600;
        margin-left: 5px;
    }
    
    /* Controls Bar */
    .controls-bar {
        background: white;
        border-radius: 12px;
        padding: 20px 30px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Insurance Request Cards */
    .insurance-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        position: relative;
    }
    
    .insurance-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 20px;
    }
    
    .card-title {
        color: #999;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .card-amount {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .card-token {
        font-size: 16px;
        color: #666;
        font-weight: 500;
        margin-left: 8px;
    }
    
    .token-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 700;
        color: white;
    }
    
    .icon-purple {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .icon-orange {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
    }
    
    .icon-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .icon-red {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Collateral Section */
    .collateral-section {
        margin: 20px 0;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 12px;
    }
    
    .collateral-label {
        color: #666;
        font-size: 13px;
        margin-bottom: 12px;
    }
    
    .collateral-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .badge-danger {
        background: #fee;
        color: #d32f2f;
    }
    
    .badge-warning {
        background: #fff3e0;
        color: #f57c00;
    }
    
    .badge-success {
        background: #e8f5e9;
        color: #388e3c;
    }
    
    .pool-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .pool-amount {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .pool-usd {
        color: #999;
        font-size: 12px;
        margin-left: 5px;
    }
    
    /* Term and Interest */
    .info-row {
        display: flex;
        justify-content: space-between;
        margin: 16px 0;
    }
    
    .info-col {
        flex: 1;
    }
    
    .info-label {
        color: #666;
        font-size: 13px;
        margin-bottom: 4px;
    }
    
    .info-value {
        color: #1a1a1a;
        font-size: 20px;
        font-weight: 700;
    }
    
    .info-subtext {
        color: #999;
        font-size: 12px;
    }
    
    /* Service Fee */
    .service-fee {
        text-align: center;
        color: #999;
        font-size: 12px;
        margin: 16px 0;
    }
    
    /* Connect Button */
    .connect-btn {
        width: 100%;
        padding: 14px;
        background: #e0e0e0;
        border: none;
        border-radius: 8px;
        color: #999;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        cursor: not-allowed;
    }
    
    .connect-btn-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
    }
    
    .connect-btn-active:hover {
        opacity: 0.9;
    }
    
    /* Type Badge */
    .type-badge {
        position: absolute;
        top: 24px;
        right: 24px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .type-fixed {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    .type-variable {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    
    /* Modal Styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    }
    
    /* Streamlit overrides */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: white;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #666;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1a1a1a;
        color: white;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    
    /* New Request Button */
    .new-request-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 32px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'show_provide_modal' not in st.session_state:
    st.session_state.show_provide_modal = False
if 'show_create_modal' not in st.session_state:
    st.session_state.show_create_modal = False
if 'selected_request' not in st.session_state:
    st.session_state.selected_request = None
if 'insurance_requests' not in st.session_state:
    # Mock insurance requests
    st.session_state.insurance_requests = [
        {
            "id": 1,
            "amount": 750,
            "token": "SigUSD",
            "icon": "purple",
            "ratio": 2.0,
            "type": "variable",
            "pool_size": 1200,
            "pool_filled": 80,
            "term_months": 18,
            "interest_rate": 36,
            "apr": 34.33,
            "service_fee": 6.75,
            "borrower": "9iDf...9nhm"
        },
        {
            "id": 2,
            "amount": 4000,
            "token": "ERG",
            "icon": "orange",
            "ratio": 1.5,
            "type": "variable",
            "pool_size": 3500,
            "pool_filled": 45,
            "term_months": 12,
            "interest_rate": 45,
            "apr": 45.62,
            "service_fee": 36,
            "borrower": "9evr...Pt5n"
        },
        {
            "id": 3,
            "amount": 1000,
            "token": "SigUSD",
            "icon": "purple",
            "ratio": 1.0,
            "type": "fixed",
            "pool_size": 850,
            "pool_filled": 85,
            "term_months": 18,
            "interest_rate": 70,
            "apr": 47.31,
            "service_fee": 9,
            "borrower": "9fny...fZC1"
        },
        {
            "id": 4,
            "amount": 150,
            "token": "ERG",
            "icon": "orange",
            "ratio": 3.0,
            "type": "variable",
            "pool_size": 100,
            "pool_filled": 67,
            "term_months": 10,
            "interest_rate": 10,
            "apr": 12.16,
            "service_fee": 1.35,
            "borrower": "9fez...e5rm"
        }
    ]

def calculate_payouts(request, my_contribution):
    """Calculate payouts based on insurance type"""
    amount = request['amount']
    ratio = request['ratio']
    pool_size = request['pool_size']
    ins_type = request['type']
    
    if ins_type == "fixed":
        # Fixed: Winner takes all
        if my_contribution >= pool_size:
            my_share = 1.0
        else:
            my_share = my_contribution / pool_size
        
        # If no claim: insurers get all of insurance amount
        my_earnings_no_claim = amount * my_share
        # If claim: buyer gets all of pool (insurers lose)
        my_loss_if_claim = my_contribution
        
        return {
            'my_earnings_no_claim': my_earnings_no_claim,
            'my_loss_if_claim': my_loss_if_claim,
            'buyer_payout_if_claim': pool_size,
            'pool_gets_no_claim': amount,
            'my_share_pct': my_share * 100
        }
    else:
        # Variable: Ratio-based with caps
        insurer_max = pool_size * (1 / ratio)
        buyer_max = amount * ratio
        
        insurer_payout = min(insurer_max, amount)
        buyer_payout = min(buyer_max, pool_size)
        
        my_share = my_contribution / pool_size if pool_size > 0 else 0
        my_earnings = my_share * insurer_payout
        
        return {
            'my_earnings_no_claim': my_earnings,
            'my_loss_if_claim': my_contribution - (my_contribution * (pool_size - buyer_payout) / pool_size if pool_size > 0 else 0),
            'buyer_payout_if_claim': buyer_payout,
            'pool_gets_no_claim': insurer_payout,
            'my_share_pct': my_share * 100
        }

# Header
st.markdown("""
    <div class="top-header">
        <div class="logo-section">
            <span style="font-size: 32px;">Σ</span>
            <span>Insurance Market</span>
            <span class="tvl-display">
                TVL: <span class="tvl-value">$21,253.53</span>
            </span>
        </div>
        <button class="connect-wallet-btn" style="padding: 10px 24px; background: #1a1a1a; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
            CONNECT WALLET
        </button>
    </div>
    """, unsafe_allow_html=True)

# Controls Bar
col1, col2 = st.columns([3, 1])
with col1:
    tab1, tab2 = st.tabs(["Insurance requests", "Active Insurances"])
with col2:
    if st.button("+ NEW INSURANCE REQUEST", key="new_req_btn"):
        st.session_state.show_create_modal = True
        st.rerun()

# Insurance Request Cards Grid
if tab1:
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    cols = st.columns(4, gap="medium")
    
    for idx, request in enumerate(st.session_state.insurance_requests):
        with cols[idx % 4]:
            # Determine risk level based on pool fill
            pool_fill_pct = request['pool_filled']
            if pool_fill_pct < 50:
                risk_color = "danger"
                risk_text = f"△ -{100-pool_fill_pct}%"
            elif pool_fill_pct < 80:
                risk_color = "warning"
                risk_text = f"△ -{100-pool_fill_pct}%"
            else:
                risk_color = "success"
                risk_text = f"△ -{100-pool_fill_pct}%"
            
            # Create card using container
            with st.container():
                # Card wrapper
                st.markdown(f"""
                    <div class="insurance-card">
                        <div class="type-badge type-{request['type']}">{request['type'].upper()}</div>
                        <div class="card-header">
                            <div>
                                <div class="card-title">Insurance request</div>
                                <div>
                                    <span class="card-amount">{request['amount']:,}</span>
                                    <span class="card-token">{request['token']}</span>
                                </div>
                            </div>
                            <div class="token-icon icon-{request['icon']}">
                                "Σ"
                            </div>
                        </div>
                        <div class="collateral-section">
                            <div class="collateral-label">Pool Status</div>
                            <div class="collateral-badge badge-{risk_color}">{risk_text}</div>
                            <div class="pool-info">
                                <div>
                                    <span class="pool-amount">{request['pool_size']:,}</span>
                                    <span class="pool-usd">≈0 USD</span>
                                </div>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-col">
                                <div class="info-label">Term</div>
                                <div class="info-value">{request['term_months']} months</div>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-col">
                                <div class="info-label">Payout Ratio</div>
                                <div class="info-value">{request['ratio']:.1f}:1</div>
                                <div class="info-subtext">{request['apr']:.2f}% APR</div>
                            </div>
                            <div class="info-col" style="text-align: right;">
                                <div class="info-label">Requester</div>
                                <div class="info-value" style="font-size: 14px;">{request['borrower']}</div>
                            </div>
                        </div>
                        <div class="service-fee">Service Fee: {request['service_fee']} {request['token']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Button below card
                if st.button(f"📋 View Details", key=f"view_{request['id']}", use_container_width=True):
                    st.session_state.selected_request = request
                    st.session_state.show_provide_modal = True
                    st.rerun()

# Provide Coverage Modal
if st.session_state.show_provide_modal and st.session_state.selected_request:
    request = st.session_state.selected_request
    
    @st.dialog("Provide Coverage", width="large")
    def provide_coverage_modal():
        st.markdown(f"### Insurance Request: {request['amount']:,} {request['token']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Request Details")
            st.write(f"**Amount:** {request['amount']:,} {request['token']}")
            st.write(f"**Type:** {request['type'].capitalize()}")
            st.write(f"**Payout Ratio:** {request['ratio']:.1f}:1")
            st.write(f"**Term:** {request['term_months']} months")
            st.write(f"**Current Pool:** {request['pool_size']:,} {request['token']}")
            st.write(f"**Pool Filled:** {request['pool_filled']}%")
            
            st.markdown("---")
            
            if request['type'] == 'fixed':
                st.info("🎲 **FIXED Insurance** - Winner takes all! Like a bet.")
                st.write("- If NO CLAIM: Pool gets ALL insurance amount")
                st.write("- If CLAIM: Buyer gets ALL pool funds")
            else:
                st.info("⚖️ **VARIABLE Insurance** - Ratio-based protection")
                st.write(f"- Payout capped by pool size and ratio")
                st.write(f"- Your earnings proportional to stake")
        
        with col2:
            st.markdown("#### Your Contribution")
            
            max_contribution = request['amount'] * 2  # Allow overbidding
            my_contribution = st.number_input(
                f"Your Stake ({request['token']})",
                min_value=10,
                max_value=max_contribution,
                value=min(500, max_contribution),
                step=10
            )
            
            # Calculate payouts
            payouts = calculate_payouts(request, my_contribution)
            
            st.markdown("---")
            st.markdown("#### Your Potential Outcomes")
            
            # Your share
            st.metric("Your Pool Share", f"{payouts['my_share_pct']:.2f}%")
            
            # No claim scenario
            st.success(f"**If NO CLAIM:** You earn {payouts['my_earnings_no_claim']:.2f} {request['token']}")
            roi_no_claim = ((payouts['my_earnings_no_claim'] - my_contribution) / my_contribution * 100)
            st.write(f"ROI: {roi_no_claim:+.2f}%")
            
            # Claim scenario
            st.error(f"**If CLAIM:** You lose {payouts['my_loss_if_claim']:.2f} {request['token']}")
            roi_claim = -((payouts['my_loss_if_claim'] / my_contribution * 100))
            st.write(f"ROI: {roi_claim:.2f}%")
            
            st.markdown("---")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.show_provide_modal = False
                    st.rerun()
            with col_b:
                if st.button("✓ Provide Coverage", type="primary", use_container_width=True):
                    st.success(f"Coverage provided: {my_contribution} {request['token']}!")
                    st.session_state.show_provide_modal = False
                    st.balloons()
                    st.rerun()
    
    provide_coverage_modal()

# Create New Request Modal
if st.session_state.show_create_modal:
    @st.dialog("Create New Insurance Request", width="large")
    def create_request_modal():
        st.markdown("### New Insurance Request")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Insurance Details")
            
            insurance_amount = st.number_input(
                "Insurance Amount",
                min_value=100,
                max_value=100000,
                value=1000,
                step=100,
                help="Amount you want to insure"
            )
            
            token_choice = st.selectbox(
                "Token",
                ["SigUSD", "ERG", "AHT", "Other"],
                help="Choose your insurance token"
            )
            
            insurance_type = st.selectbox(
                "Insurance Type",
                ["variable", "fixed"],
                help="Variable: ratio-based | Fixed: winner takes all"
            )
            
            if insurance_type == "variable":
                insurance_ratio = st.slider(
                    "Payout Ratio",
                    min_value=0.0,
                    max_value=5.0,
                    value=2.0,
                    step=0.1,
                    help="Higher ratio = higher risk/reward"
                )
                st.caption(f"Ratio: {insurance_ratio:.1f}:1")
            else:
                insurance_ratio = 1.0
                st.info("🎲 Fixed insurance - Winner takes all!")
            
            term_months = st.number_input(
                "Term (months)",
                min_value=1,
                max_value=36,
                value=12,
                step=1
            )
        
        with col2:
            st.markdown("#### Preview")
            
            st.write(f"**Amount:** {insurance_amount:,} {token_choice}")
            st.write(f"**Type:** {insurance_type.capitalize()}")
            st.write(f"**Ratio:** {insurance_ratio:.1f}:1")
            st.write(f"**Term:** {term_months} months")
            
            st.markdown("---")
            
            if insurance_type == "fixed":
                st.info("**FIXED Insurance (Bet)**")
                st.write(f"- If claim: You win the entire pool")
                st.write(f"- If no claim: Pool wins your {insurance_amount:,} {token_choice}")
            else:
                st.info("**VARIABLE Insurance (Protected)**")
                estimated_pool = insurance_amount * insurance_ratio
                max_payout = min(insurance_amount * insurance_ratio, estimated_pool)
                st.write(f"- Estimated pool needed: {estimated_pool:,} {token_choice}")
                st.write(f"- Your max payout: {max_payout:,} {token_choice}")
                st.write(f"- Ratio protection: {insurance_ratio:.1f}:1")
            
            st.markdown("---")
            
            service_fee = insurance_amount * 0.01  # 1% fee
            st.write(f"**Service Fee:** {service_fee:.2f} {token_choice}")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_create_modal = False
                st.rerun()
        with col_b:
            if st.button("✓ Create Request", type="primary", use_container_width=True):
                # Add new request to list
                new_request = {
                    "id": len(st.session_state.insurance_requests) + 1,
                    "amount": insurance_amount,
                    "token": token_choice,
                    "icon": random.choice(["purple", "orange", "blue", "red"]),
                    "ratio": insurance_ratio,
                    "type": insurance_type,
                    "pool_size": 0,
                    "pool_filled": 0,
                    "term_months": term_months,
                    "interest_rate": int(insurance_ratio * 20),
                    "apr": insurance_ratio * 15,
                    "service_fee": service_fee,
                    "borrower": "You"
                }
                st.session_state.insurance_requests.append(new_request)
                st.success(f"Insurance request created: {insurance_amount} {token_choice}!")
                st.session_state.show_create_modal = False
                st.balloons()
                st.rerun()
    
    create_request_modal()

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
        SigmaShield Protocol • Decentralized Insurance
    </div>
    """, unsafe_allow_html=True)