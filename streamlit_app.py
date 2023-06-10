import streamlit as st
import altair as alt
import pandas as pd

# --------------setup
st.set_page_config(
    page_title='Household Budget Balancer', 
    page_icon='💰', 
    initial_sidebar_state="auto", 
    menu_items=None,
    # layout='wide'
)
st.title("Household Budget Balancer 💰")

col1, col2 = st.columns(2)

with col1:
    income_a = st.number_input(
        "💁‍♀️ Person A's Annual Income (after taxes)",
        min_value=0, max_value=1000000,
        step=1, value=50000
    )
with col2:
    income_b = st.number_input(
        "🤷‍♂️ Person B's Annual Income (after taxes)",
        min_value=0, max_value=1000000,
        step=1, value=40000
    )
joint_expenses = st.number_input(
    "💳 Joint Monthly Expenses (ex: rent, groceries, ...)",  
    min_value=0, max_value=1000000,
    step=1, value=2000
)

# -----------------math n stuff

viz_df = pd.DataFrame([])
viz_df['Person'] = ['💁‍♀️ Person A', '🤷‍♂️ Person B']
viz_df['Annual Income'] = [income_a, income_b]
viz_df['Monthly Income'] = viz_df['Annual Income'] / 12
viz_df['% of Combined Income'] = (viz_df['Annual Income'] / viz_df['Annual Income'].sum())
viz_df['% of Joint Expenses'] = viz_df['% of Combined Income']
viz_df['Amount of Joint Expenses'] = viz_df['% of Joint Expenses'] * joint_expenses
viz_df['Amount Left Over (per month)'] =  viz_df['Monthly Income'] - viz_df['Amount of Joint Expenses']
viz_df['% of Income Put Towards Joint Expenses'] = (viz_df['Amount Left Over (per month)'] / viz_df['Monthly Income']).round(4)
viz_df['% of Income Left Over Per Person'] = 1 - viz_df['% of Income Put Towards Joint Expenses']
viz_df['% of Joint Expenses'] = (viz_df['% of Joint Expenses'] * 100).round(0).astype(int).astype(str) + '%'
viz_df['% of Combined Income'] = (viz_df['% of Combined Income'] * 100).round(0).astype(int).astype(str) + '%'

# ----------------vizin

base = alt.Chart(viz_df).encode(
    theta=alt.Theta(field='Annual Income', type="quantitative", stack=True),
    color=alt.Color(field="Person", type="nominal"),
    tooltip=[
            'Person',
            '% of Combined Income',
            'Annual Income'
        ]
)
donut = base.mark_arc(outerRadius=100, innerRadius=50)
text = base.mark_text(radius=120, size=15).encode(text='% of Combined Income'+":N")
st.altair_chart(
    (donut + text).properties(
    title="Combined Annual Income Breakdown"
).interactive(), use_container_width=True)


st.markdown('### 📊 Fair Distribution of Joint Expenses')

bars = alt.Chart(viz_df).mark_bar().encode(
    y='Person',
    x = alt.Y("Amount of Joint Expenses", axis=alt.Axis(format='$s'))
)
plot = (bars).properties(
    title="Amount ($) of Expenses Covered Per Person"
).interactive()
st.altair_chart(plot, use_container_width=True)

base = alt.Chart(viz_df).encode(
    theta=alt.Theta(field='Amount of Joint Expenses', type="quantitative", stack=True),
    color=alt.Color(field="Person", type="nominal"),
    tooltip=[
            'Person',
            '% of Joint Expenses',
            'Amount of Joint Expenses'
        ]
)
donut = base.mark_arc(outerRadius=100, innerRadius=50)
text = base.mark_text(radius=120, size=15).encode(text='% of Joint Expenses'+":N")
st.altair_chart(
    (donut + text).properties(
    title="% of Expenses Covered Per Person"
).interactive(), use_container_width=True)

st.markdown("### 🤑 What's Left Over per Person?")

bars = alt.Chart(viz_df).mark_bar().encode(
    y='Person',
    x = alt.Y("% of Income Left Over Per Person", axis=alt.Axis(format='%'))
)
plot = (bars).properties(
    title="% of Income Left Over Per Person"
).interactive()
st.altair_chart(plot, use_container_width=True)

bars = alt.Chart(viz_df).mark_bar().encode(
    y='Person',
    x = alt.Y("Amount Left Over (per month)", axis=alt.Axis(format='$s'))
)
plot = (bars).properties(
    title="Amount Left Over Per Person (per month)"
).interactive()
st.altair_chart(plot, use_container_width=True)