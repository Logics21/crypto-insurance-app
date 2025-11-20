# CryptoShield - Decentralized Insurance App

A Python-based web application for creating and managing decentralized crypto insurance contracts.

## Features

- 🔒 **Buy Insurance**: Create insurance requests with custom coverage amounts and terms
- 📈 **Provide Coverage**: Act as an insurer and earn yields on capital
- 💰 **Real-time Calculations**: See potential earnings for both buyers and insurers
- ⚖️ **Variable/Fixed Insurance**: Choose between variable ratio-based or fixed payouts
- 📊 **Risk Analysis**: Visual risk indicators and ROI calculations

## Renamed Variables (Clearer Naming)

The original code variables have been renamed for clarity:

- `insurance_ammount` → `coverage_amount` - Amount the buyer wants insured
- `insurance_ratio` → `payout_ratio` - Multiplier for variable insurance
- `insurance_cond1` → `insurance_type` - Variable or Fixed
- `insurance_pool` → `insurer_pool_total` - Total insurer capital
- `my_contr` → `my_insurer_stake` - Individual insurer's contribution
- `insurance_maduration` → `duration_days` - Lock period in days

## Installation

1. **Install Python** (3.8 or higher)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install Streamlit directly:
   ```bash
   pip install streamlit
   ```

## Running the App

1. **Navigate to the app directory**:
   ```bash
   cd /path/to/app/directory
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run crypto_insurance_app.py
   ```

3. **Access the app**:
   - Your browser should automatically open to `http://localhost:8501`
   - If not, manually navigate to that URL

## How to Use

### As a Buyer (Insuree):

1. Select "🔒 Buy Insurance (Insuree)" from the sidebar
2. Set your **Coverage Amount** (how much USDC to insure)
3. Choose **Insurance Type**:
   - **Variable**: Set a payout ratio (higher ratio = higher reward/risk)
   - **Fixed**: Standard 1:1 payout
4. Set the **Duration** (how long funds are locked)
5. Click "Lock Funds & Create Request"
6. View your potential payout on the right panel

### As an Insurer:

1. Select "📈 Provide Coverage (Insurer)" from the sidebar
2. View the available insurance request details
3. Set the **Total Insurer Pool** (combined capital from all insurers)
4. Set **Your Stake** (your contribution to the pool)
5. See your pool share percentage
6. Click "Provide Coverage"
7. View your potential earnings on the right panel

## Understanding the Calculations

### Variable Insurance:
```python
insurer_max_payout = insurer_pool_total * (1 / payout_ratio)
buyer_max_payout = coverage_amount * payout_ratio

insurer_actual_payout = min(insurer_max_payout, coverage_amount)
buyer_actual_payout = min(buyer_max_payout, insurer_pool_total)

my_earnings = (my_insurer_stake / insurer_pool_total) * insurer_actual_payout
```

### Fixed Insurance:
```python
insurer_payout = coverage_amount
buyer_payout = insurer_pool_total
my_earnings = (my_insurer_stake / insurer_pool_total) * insurer_payout
```

## Scenarios

### Buyer Wins (Claim Triggers):
- Buyer receives the payout amount
- Insurers lose their stake proportionally

### Insurers Win (No Claim):
- Insurers split the buyer's locked funds
- Earnings distributed by pool share percentage

## Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework for data apps
- **Custom CSS** - Crypto-themed dark mode styling

## File Structure

```
.
├── crypto_insurance_app.py    # Main application
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Troubleshooting

**Port already in use:**
```bash
streamlit run crypto_insurance_app.py --server.port 8502
```

**Module not found error:**
```bash
pip install --upgrade streamlit
```

**App not opening in browser:**
- Manually navigate to `http://localhost:8501`
- Or use: `streamlit run crypto_insurance_app.py --server.headless false`

## License

Open source - feel free to modify and use as needed.
