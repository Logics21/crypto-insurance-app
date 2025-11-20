import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Ergo Insurance - Oracle-Based Protection",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling - Ergo theme
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1810 50%, #1a1a1a 100%);
    }
    .stMetric {
        background-color: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 94, 0, 0.3);
    }
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin: 10px 0;
    }
    .info-box {
        background: linear-gradient(135deg, rgba(255, 94, 0, 0.2) 0%, rgba(255, 128, 0, 0.2) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 94, 0, 0.3);
        margin: 10px 0;
    }
    .warning-box {
        background: rgba(251, 191, 36, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #fbbf24;
        margin: 10px 0;
    }
    .oracle-box {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin: 10px 0;
    }
    h1 {
        color: #ff5e00;
    }
    h2, h3 {
        color: #ffb380;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("# 🔷")
with col2:
    st.title("Ergo Insurance")
    st.markdown("**Oracle-Based Decentralized Protection**")

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
**Ergo Insurance** enables:
- Oracle-based smart insurance contracts
- Weather, price, and custom triggers
- Flexible payout ratios (0.25x to 5x)
- Decentralized protection on Ergo blockchain
- Fair risk/reward distribution
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
        
        # Oracle Trigger Event
        st.markdown("---")
        st.subheader("🔮 Oracle Trigger Event")
        
        trigger_event = st.selectbox(
            "Select Trigger Source",
            [
                "Weather - Temperature",
                "Weather - Rainfall",
                "Weather - Wind Speed",
                "Price Movement - ERG/USD",
                "Price Movement - BTC/USD",
                "Price Movement - ETH/USD",
                "Agricultural - Crop Yield",
                "Flight Delay",
                "Custom Oracle Data"
            ],
            help="What event will trigger the insurance payout?"
        )
        
        # Trigger condition
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            trigger_condition = st.selectbox(
                "Condition",
                ["Above", "Below", "Equals", "Between"],
                help="When should payout be triggered?"
            )
        
        with col_t2:
            if trigger_condition == "Between":
                trigger_value = st.text_input("Value Range", value="20-30", help="e.g., 20-30")
            else:
                trigger_value = st.number_input("Threshold Value", value=100.0, step=1.0)
        
        # Oracle source
        oracle_source = st.text_input(
            "🌐 Oracle Address (optional)",
            value="",
            placeholder="0x... or oracle.ergo.io/weather",
            help="Smart contract or API endpoint for oracle data"
        )
        
        st.markdown("---")
        
        # Payout Ratio (only for variable) - NOW GOES LOWER THAN 1
        if insurance_type == "Variable":
            payout_ratio = st.slider(
                "⚖️ Payout Ratio",
                min_value=0.1,
                max_value=5.0,
                value=2.0,
                step=0.1,
                help="Lower than 1.0 means conservative (e.g., 0.25 = 1:4 ratio). Higher means aggressive (e.g., 5.0 = 5:1 ratio)"
            )
            
            # Show ratio in both directions for clarity
            if payout_ratio < 1.0:
                ratio_display = f"1:{int(1/payout_ratio)}"
                risk_level = "🟢 Very Conservative"
                risk_color = "green"
            elif payout_ratio < 2.0:
                ratio_display = f"{payout_ratio:.1f}:1"
                risk_level = "🟢 Low Risk"
                risk_color = "green"
            elif payout_ratio < 3.5:
                ratio_display = f"{payout_ratio:.1f}:1"
                risk_level = "🟡 Medium Risk"
                risk_color = "orange"
            else:
                ratio_display = f"{payout_ratio:.1f}:1"
                risk_level = "🔴 High Risk"
                risk_color = "red"
            
            st.markdown(f"**Risk Level:** :{risk_color}[{risk_level}]")
            st.caption(f"Payout multiplier: **{ratio_display}**")
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
        
        # Oracle trigger info
        st.markdown('<div class="oracle-box">', unsafe_allow_html=True)
        st.markdown("**🔮 Oracle Trigger:**")
        st.markdown(f"**Event:** {trigger_event}")
        st.markdown(f"**Condition:** {trigger_condition} {trigger_value}")
        if oracle_source:
            st.markdown(f"**Source:** `{oracle_source}`")
        else:
            st.markdown("**Source:** Default Ergo Oracle Pool")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional details
        with st.expander("📋 View Insurance Details"):
            st.write(f"**Coverage Amount:** ${coverage_amount:,.2f}")
            st.write(f"**Insurance Type:** {insurance_type}")
            if insurance_type == "Variable":
                if payout_ratio < 1.0:
                    st.write(f"**Payout Ratio:** 1:{int(1/payout_ratio)}")
                else:
                    st.write(f"**Payout Ratio:** {payout_ratio:.1f}:1")
            st.write(f"**Duration:** {duration_days} days")
            st.write(f"**Expected Pool:** ${insurer_pool_total:,.2f}")
            st.markdown("---")
            st.write(f"**🔮 Trigger Event:** {trigger_event}")
            st.write(f"**Condition:** {trigger_condition} {trigger_value}")
            if oracle_source:
                st.write(f"**Oracle Source:** {oracle_source}")
            else:
                st.write(f"**Oracle Source:** Default Ergo Oracle Pool")

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
                min_value=0.1,
                max_value=5.0,
                value=2.0,
                step=0.1,
                disabled=True
            )
            
            # Show readable ratio format
            if payout_ratio < 1.0:
                st.caption(f"Ratio: 1:{int(1/payout_ratio)}")
            else:
                st.caption(f"Ratio: {payout_ratio:.1f}:1")
        else:
            payout_ratio = 1.0
        
        duration_days = st.number_input(
            "Duration (Days)",
            min_value=1,
            max_value=365,
            value=30,
            disabled=True
        )
        
        # Show oracle trigger information
        st.markdown("---")
        st.markdown("**🔮 Oracle Trigger:**")
        
        trigger_event = st.selectbox(
            "Trigger Event",
            [
                "Weather - Temperature",
                "Weather - Rainfall", 
                "Weather - Wind Speed",
                "Price Movement - ERG/USD",
                "Price Movement - BTC/USD",
                "Price Movement - ETH/USD",
                "Agricultural - Crop Yield",
                "Flight Delay",
                "Custom Oracle Data"
            ],
            index=3,
            disabled=True
        )
        
        trigger_condition = st.text_input(
            "Trigger Condition",
            value="Below 2.50",
            disabled=True
        )
        
        oracle_source = st.text_input(
            "Oracle Source",
            value="Default Ergo Oracle Pool",
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
    1. **Lock Funds:** Deposit ERG/USDC as your insurance premium
    2. **Set Terms:** Choose insurance type, payout ratio, and oracle trigger
    3. **Configure Oracle:** Select event (weather, price, etc.) and conditions
    4. **Wait for Oracle:** Smart contract monitors oracle data feed
    5. **Outcome:** Get paid if oracle confirms trigger, otherwise insurers keep premium
    
    ### For Insurers:
    1. **Provide Capital:** Add ERG/USDC to the insurance pool
    2. **Accept Terms:** Review oracle trigger and payout conditions
    3. **Earn Premiums:** Collect buyer's locked funds if oracle doesn't trigger
    4. **Pool Share:** Your earnings are proportional to your stake
    5. **Risk:** If oracle confirms trigger, you pay out from your stake
    
    ### Insurance Types:
    - **Variable:** Payout amount varies based on the ratio you set
      - **Below 1.0** (e.g., 0.25 = 1:4): Very conservative, lower payouts
      - **Above 1.0** (e.g., 3.0 = 3:1): Aggressive, higher payouts
    - **Fixed:** Predetermined payout amount (standard 1:1 insurance)
    
    ### Oracle Triggers:
    - **Weather Data:** Temperature, rainfall, wind speed from weather oracles
    - **Price Movement:** Crypto/token prices from Ergo Oracle Pools
    - **Agricultural:** Crop yields, harvest data
    - **Custom:** Any data feed from verified Ergo oracle contracts
    
    ### How Oracles Work:
    1. Oracle pools aggregate data from multiple sources
    2. Smart contract checks oracle data at specified intervals
    3. When condition is met, payout is automatically triggered
    4. No human intervention needed - trustless execution
    """)

