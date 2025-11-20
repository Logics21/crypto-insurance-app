import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="CryptoShield - Decentralized Insurance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e1b4b 0%, #581c87 50%, #1e1b4b 100%);
    }
    .stMetric {
        background-color: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin: 10px 0;
    }
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(14, 165, 233, 0.2) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        margin: 10px 0;
    }
    .warning-box {
        background: rgba(251, 191, 36, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #fbbf24;
        margin: 10px 0;
    }
    h1 {
        color: #c084fc;
    }
    h2, h3 {
        color: #e9d5ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("# 🛡️")
with col2:
    st.title("CryptoShield")
    st.markdown("**Decentralized Insurance Marketplace**")

st.markdown("---")

# Sidebar for view selection
st.sidebar.title("⚙️ Select View")
view = st.sidebar.radio(
    "Choose your role:",
    ["🔒 Buy Insurance (Insuree)", "📈 Provide Coverage (Insurer)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**CryptoShield** allows you to:
- Create insurance requests with custom terms
- Provide liquidity as an insurer
- Earn yields on capital
- Protect against risks
""")


def calculate_payouts(coverage_amount, insurance_type, payout_ratio, insurer_pool_total, my_insurer_stake):
    """Calculate potential payouts for both buyer and insurer"""
    
    if insurance_type == "Variable":
        # Variable insurance calculations
        insurer_max_payout = insurer_pool_total * (1 / payout_ratio)
        buyer_max_payout = coverage_amount * payout_ratio
        
        insurer_actual_payout = min(insurer_max_payout, coverage_amount)
        buyer_actual_payout = min(buyer_max_payout, insurer_pool_total)
        
        my_earnings = (my_insurer_stake / insurer_pool_total) * insurer_actual_payout
    else:
        # Fixed insurance calculations
        insurer_actual_payout = coverage_amount
        buyer_actual_payout = insurer_pool_total
        my_earnings = (my_insurer_stake / insurer_pool_total) * insurer_actual_payout
    
    my_pool_share = (my_insurer_stake / insurer_pool_total) * 100
    
    return {
        'insurer_payout': insurer_actual_payout,
        'buyer_payout': buyer_actual_payout,
        'my_earnings': my_earnings,
        'my_pool_share': my_pool_share
    }


def calculate_roi(payout, investment):
    """Calculate return on investment percentage"""
    return ((payout - investment) / investment * 100) if investment > 0 else 0


# Main content area
if "🔒 Buy Insurance" in view:
    st.header("🔒 Create Insurance Request")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Insurance Configuration")
        
        # Coverage Amount
        coverage_amount = st.number_input(
            "💰 Coverage Amount (USDC)",
            min_value=100,
            max_value=1000000,
            value=1000,
            step=100,
            help="Amount you want to insure"
        )
        
        # Insurance Type
        insurance_type = st.radio(
            "📋 Insurance Type",
            ["Variable", "Fixed"],
            index=0,
            help="Variable: payout depends on ratio | Fixed: predetermined payout"
        )
        
        # Payout Ratio (only for variable)
        if insurance_type == "Variable":
            payout_ratio = st.slider(
                "⚖️ Payout Ratio",
                min_value=1.0,
                max_value=5.0,
                value=2.0,
                step=0.1,
                help="Higher ratio = higher potential payout, but riskier"
            )
            
            # Risk level indicator
            if payout_ratio < 2.0:
                risk_level = "🟢 Low Risk"
                risk_color = "green"
            elif payout_ratio < 3.5:
                risk_level = "🟡 Medium Risk"
                risk_color = "orange"
            else:
                risk_level = "🔴 High Risk"
                risk_color = "red"
            
            st.markdown(f"**Risk Level:** :{risk_color}[{risk_level}]")
            st.caption(f"Payout multiplier: **{payout_ratio:.1f}:1**")
        else:
            payout_ratio = 1.0
        
        # Duration
        duration_days = st.number_input(
            "📅 Duration (Days)",
            min_value=1,
            max_value=365,
            value=30,
            step=1,
            help="How long to lock your funds"
        )
        
        # Calculate dates
        lock_date = datetime.now()
        end_date = lock_date + timedelta(days=duration_days)
        
        st.caption(f"**Lock Date:** {lock_date.strftime('%Y-%m-%d')}")
        st.caption(f"**End Date:** {end_date.strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        
        # Action button
        if st.button("🔐 Lock Funds & Create Request", type="primary", use_container_width=True):
            st.success("✅ Insurance request created successfully!")
            st.balloons()
    
    with col2:
        st.subheader("📊 Buyer (Insuree) Earnings Preview")
        
        # Default insurer pool for preview
        insurer_pool_total = coverage_amount * 2
        my_insurer_stake = coverage_amount
        
        # Calculate payouts
        payouts = calculate_payouts(
            coverage_amount, 
            insurance_type, 
            payout_ratio, 
            insurer_pool_total, 
            my_insurer_stake
        )
        
        buyer_roi = calculate_roi(payouts['buyer_payout'], coverage_amount)
        
        # Display metrics
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("#### Your Locked Amount")
        st.markdown(f"### ${coverage_amount:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("#### 💎 Potential Payout (if claim)")
        st.markdown(f"### ${payouts['buyer_payout']:,.2f}")
        st.markdown(f"**ROI:** :green[+{buyer_roi:.2f}%]" if buyer_roi > 0 else f"**ROI:** :red[{buyer_roi:.2f}%]")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**📌 Scenario:**")
        st.markdown("""
        - **If claim triggers:** You receive the payout amount
        - **If no claim:** Insurers keep your locked funds
        - Your funds are locked for the duration period
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional details
        with st.expander("📋 View Insurance Details"):
            st.write(f"**Coverage Amount:** ${coverage_amount:,.2f}")
            st.write(f"**Insurance Type:** {insurance_type}")
            if insurance_type == "Variable":
                st.write(f"**Payout Ratio:** {payout_ratio:.1f}:1")
            st.write(f"**Duration:** {duration_days} days")
            st.write(f"**Expected Pool:** ${insurer_pool_total:,.2f}")

else:  # Insurer View
    st.header("📈 Provide Insurance Coverage")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Pool Configuration")
        
        # Existing insurance request details (for context)
        st.markdown("**📄 Available Insurance Request:**")
        coverage_amount = st.number_input(
            "Coverage Amount (USDC)",
            min_value=100,
            max_value=1000000,
            value=1000,
            step=100,
            disabled=True,
            help="Buyer's requested coverage amount"
        )
        
        insurance_type = st.selectbox(
            "Insurance Type",
            ["Variable", "Fixed"],
            index=0,
            disabled=True
        )
        
        if insurance_type == "Variable":
            payout_ratio = st.slider(
                "Payout Ratio",
                min_value=1.0,
                max_value=5.0,
                value=2.0,
                step=0.1,
                disabled=True
            )
        else:
            payout_ratio = 1.0
        
        duration_days = st.number_input(
            "Duration (Days)",
            min_value=1,
            max_value=365,
            value=30,
            disabled=True
        )
        
        st.markdown("---")
        st.markdown("**💼 Your Pool Contribution:**")
        
        # Total Pool
        insurer_pool_total = st.number_input(
            "💰 Total Insurer Pool (USDC)",
            min_value=100,
            max_value=10000000,
            value=2000,
            step=100,
            help="Total capital from all insurers"
        )
        
        # My Stake
        my_insurer_stake = st.number_input(
            "💵 Your Stake (USDC)",
            min_value=100,
            max_value=insurer_pool_total,
            value=min(1000, insurer_pool_total),
            step=100,
            help="Your contribution to the insurance pool"
        )
        
        # Calculate pool share
        pool_share = (my_insurer_stake / insurer_pool_total) * 100
        st.progress(pool_share / 100)
        st.caption(f"Your pool share: **{pool_share:.2f}%**")
        
        st.markdown("---")
        
        # Action button
        if st.button("📝 Provide Coverage", type="primary", use_container_width=True):
            st.success("✅ Coverage provided successfully!")
            st.balloons()
    
    with col2:
        st.subheader("📊 Insurer Earnings Preview")
        
        # Calculate payouts
        payouts = calculate_payouts(
            coverage_amount, 
            insurance_type, 
            payout_ratio, 
            insurer_pool_total, 
            my_insurer_stake
        )
        
        my_roi = calculate_roi(payouts['my_earnings'], my_insurer_stake)
        insurer_roi = calculate_roi(payouts['insurer_payout'], insurer_pool_total)
        
        # Pool overview
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(
                label="🏦 Total Pool",
                value=f"${insurer_pool_total:,.2f}",
                delta=None
            )
        with col_b:
            st.metric(
                label="💼 Your Stake",
                value=f"${my_insurer_stake:,.2f}",
                delta=f"{pool_share:.1f}% share"
            )
        
        # Earnings potential
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("#### 💰 Your Potential Earnings")
        st.markdown("##### (if no claim)")
        st.markdown(f"### ${payouts['my_earnings']:,.2f}")
        st.markdown(f"**Your ROI:** :green[+{my_roi:.2f}%]" if my_roi > 0 else f"**Your ROI:** :red[{my_roi:.2f}%]")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pool payout info
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("#### 📤 Total Pool Payout")
        st.markdown("##### (if claim occurs)")
        st.markdown(f"### ${payouts['insurer_payout']:,.2f}")
        st.markdown(f"**Pool ROI:** :red[{insurer_roi:.2f}%]" if insurer_roi < 0 else f"**Pool ROI:** :green[+{insurer_roi:.2f}%]")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**📌 Scenario:**")
        st.markdown("""
        - **If no claim:** Insurers split buyer's locked funds proportionally
        - **If claim triggers:** Insurers pay out from their pool
        - Your earnings are proportional to your stake percentage
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer with risk/reward summary
st.markdown("---")
st.markdown("## 📊 Risk/Reward Summary")

col1, col2, col3, col4 = st.columns(4)

# Use default values for summary
if "🔒 Buy Insurance" in view:
    summary_coverage = coverage_amount
    summary_type = insurance_type
    summary_ratio = payout_ratio
    summary_pool = coverage_amount * 2
else:
    summary_coverage = coverage_amount
    summary_type = insurance_type
    summary_ratio = payout_ratio
    summary_pool = insurer_pool_total

with col1:
    st.metric("Insurance Type", summary_type)

with col2:
    if summary_type == "Variable":
        if summary_ratio < 2.0:
            risk_label = "Low"
            risk_delta = "Conservative"
        elif summary_ratio < 3.5:
            risk_label = "Medium"
            risk_delta = "Moderate"
        else:
            risk_label = "High"
            risk_delta = "Aggressive"
        st.metric("Risk Level", risk_label, risk_delta)
    else:
        st.metric("Risk Level", "Fixed", "Standard")

with col3:
    if summary_type == "Variable":
        st.metric("Payout Ratio", f"{summary_ratio:.1f}:1")
    else:
        st.metric("Payout Ratio", "1:1")

with col4:
    coverage_ratio = summary_pool / summary_coverage
    st.metric("Pool Coverage", f"{coverage_ratio:.2f}x")

# Info section at bottom
st.markdown("---")
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    ### For Buyers (Insurees):
    1. **Lock Funds:** Deposit USDC as your insurance premium
    2. **Set Terms:** Choose insurance type and payout conditions
    3. **Wait:** If your conditions trigger, you get the payout
    4. **Outcome:** Get paid if claim is valid, otherwise insurers keep premium
    
    ### For Insurers:
    1. **Provide Capital:** Add USDC to the insurance pool
    2. **Earn Premiums:** Collect buyer's locked funds if no claim
    3. **Pool Share:** Your earnings are proportional to your stake
    4. **Risk:** If claim triggers, you pay out from your stake
    
    ### Insurance Types:
    - **Variable:** Payout amount varies based on the ratio you set (higher risk/reward)
    - **Fixed:** Predetermined payout amount (standard insurance)
    """)
