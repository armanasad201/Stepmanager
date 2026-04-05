import streamlit as st

st.title("Step-wise Profit Calculator 💰")

balance = st.number_input("Start Balance", value=100.0)
payout = st.number_input("Payout", value=1.96)
steps = st.number_input("Steps", value=4, step=1)
target_profit = st.number_input("Target Profit per Step", value=6.0)

if st.button("Calculate"):

    if payout <= 1:
        st.error("Payout must be greater than 1")
    else:
        bets = []
        profits = []
        cumulative = 0

        for i in range(int(steps)):
            bet = (target_profit + cumulative) / (payout - 1)
            bet = round(bet)
            bets.append(bet)
            cumulative += bet
            profit = bet * payout - cumulative
            profits.append(round(profit,2))

        total_risk = sum(bets)
        avg_profit = round(sum(profits)/len(profits),2)
        leftover = balance - total_risk

        st.subheader("📊 Results")

        for i in range(len(bets)):
            st.write(f"Step {i+1}: Bet = {bets[i]} | Profit = {profits[i]}")

        st.write(f"**Total Risk:** {total_risk}")
        st.write(f"**Average Profit:** {avg_profit}")
        st.write(f"**Leftover Balance:** {leftover}")

        # Profit analysis
        st.subheader("📈 Profit Analysis")
        st.write(f"Max Profit: {max(profits)}")
        st.write(f"Min Profit: {min(profits)}")
        st.write(f"Difference: {round(max(profits)-min(profits),2)}")

        # Risk warning
        if total_risk > balance:
            st.error("⚠️ Risk exceeds balance!")
        else:
            st.success("✔ Safe within balance")