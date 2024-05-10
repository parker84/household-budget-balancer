import streamlit as st
import altair as alt
import pandas as pd
from millify import millify

# --------------setup
st.set_page_config(
    page_title='Household Budget Balancer', 
    page_icon='💰', 
    initial_sidebar_state="auto", 
    menu_items=None,
    layout='wide'
)
st.title("Household Budget Balancer 💰")
st.caption('The purpose of this app is to enable to couples to fairly distribute their joint expenses ⚖️')

col1, col2 = st.columns((2, 1))

with col1:
    col3, col4 = st.columns(2)
    with col3:
        income_a = st.number_input(
            "💁‍♀️ Person A's Annual Income (after taxes)",
            min_value=0, max_value=1000000,
            step=1, value=50000
        )
    with col4:
        income_b = st.number_input(
            "🤷‍♂️ Person B's Annual Income (after taxes)",
            min_value=0, max_value=1000000,
            step=1, value=40000
        )
    with st.expander('➕ Calculate Joint Monthly Expenses'):
        rent = st.number_input(
            "🏡 Rent / Mortgage",
            min_value=0, max_value=1000000,
            step=1, value=2000
        )
        groceries = st.number_input(
            "🍎 Groceries",
            min_value=0, max_value=1000000,
            step=1, value=800
        )
        transportation = st.number_input(
            "🚙 Transportation",
            min_value=0, max_value=1000000,
            step=1, value=900
        )
        utilities = st.number_input(
            "💡 Utilities",
            min_value=0, max_value=1000000,
            step=1, value=300
        )
        other = st.number_input(
            "Other / Miscellaneous",
            min_value=0, max_value=1000000,
            step=1, value=200
        )
        calculated_join_monthly_expenses = rent + groceries + transportation + utilities + other
        st.markdown(f'**Total Joint Monthly Expenses: `${millify(calculated_join_monthly_expenses, precision=2)}`**')
    joint_expenses = st.number_input(
        "💳 Joint Monthly Expenses (ex: rent, groceries, ...)",  
        min_value=0, max_value=1000000,
        step=1, value=calculated_join_monthly_expenses
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
viz_df['% of Income Put Towards Joint Expenses'] = (viz_df['Amount of Joint Expenses'] / viz_df['Monthly Income']).round(4)
viz_df['% of Income Left Over Per Person'] = 1 - viz_df['% of Income Put Towards Joint Expenses']
viz_df['% of Combined Income'] = (viz_df['% of Combined Income'] * 100).round(0).astype(int).astype(str) + '%'
print(viz_df.T)
# ----------------vizin

with col2:
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

st.markdown('### 💵 How Much Should Each Person Pay?')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        '💁‍♀️ Person A Amount ($)',
        value=f"${millify(viz_df[['Amount of Joint Expenses']].iloc[0], precision=2)}"
    )
with col2:
    st.metric(
        '🤷‍♂️ Person B Amount ($)',
        value=f"${millify(viz_df[['Amount of Joint Expenses']].iloc[1], precision=2)}",
    )
with col3:
    st.metric(
        '💁‍♀️ Person A % of Expenses Covered',
        value=f"{millify(100 * viz_df[['% of Joint Expenses']].iloc[0], precision=0)}%"
    )
with col4:
    st.metric(
        '🤷‍♂️ Person B % of Expenses Covered',
        value=f"{millify(100 * viz_df[['% of Joint Expenses']].iloc[1], precision=0)}%"
    )

bars = alt.Chart(viz_df).mark_bar().encode(
    y='Person',
    x = alt.Y("Amount of Joint Expenses", axis=alt.Axis(format='$s'))
)
plot = (bars).properties(
    title="Amount ($) of Expenses Covered Per Person"
).interactive()
st.altair_chart(plot, use_container_width=True)

st.markdown("### 🤑 What's Left Over per Person?")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        '💁‍♀️ Person A Amount Left Over ($)',
        value=f"${millify(viz_df[['Amount Left Over (per month)']].iloc[0], precision=2)}"
    )
with col2:
    st.metric(
        '🤷‍♂️ Person B Amount Left Over ($)',
        value=f"${millify(viz_df[['Amount Left Over (per month)']].iloc[1], precision=2)}",
    )
with col3:
    st.metric(
        '💁‍♀️ Person A % of Income Left Over',
        value=f"{millify(100 * viz_df[['% of Income Left Over Per Person']].iloc[0], precision=0)}%"
    )
with col4:
    st.metric(
        '🤷‍♂️ Person B % of Income Left Over',
        value=f"{millify(100 * viz_df[['% of Income Left Over Per Person']].iloc[1], precision=0)}%"
    )
bars = alt.Chart(viz_df).mark_bar().encode(
    y='Person',
    x = alt.Y("Amount Left Over (per month)", axis=alt.Axis(format='$s'))
)
plot = (bars).properties(
    title="Amount ($) Left Over Per Person"
).interactive()
st.altair_chart(plot, use_container_width=True)
