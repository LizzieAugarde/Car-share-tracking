import streamlit as st 

# setting sidebar visibility 
if "show_nav" not in st.session_state:
    st.session_state.show_nav = True


# controlling visibility
st.markdown("""
<style>
.sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    background-color: #f8f9fa;
    overflow-x: hidden;
    transition: transform 0.3s ease-in-out;
    width: 250px;
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    z-index: 999;
}

.sidebar-hidden {
    transform: translateX(-260px);
}
.sidebar-visible {
    transform: translateX(0);
}
</style>
""", unsafe_allow_html=True)

sidebar_class = "sidebar-visible" if st.session_state.show_nav else "sidebar-hidden"
st.markdown(f'<div class="sidebar-container {sidebar_class}">', unsafe_allow_html=True)

# setting up pages 
dashboard_page = st.Page("dashboard.py", title = "Dashboard", icon = ":material/dashboard:")
log_journey_page = st.Page("log_journey.py", title = "Log a journey", icon = ":material/add_circle:")
log_fuel_page = st.Page("log_fuel.py", title = "Log a fuel fill up", icon = ":material/add_circle:")


pg = st.navigation([dashboard_page, log_journey_page, log_fuel_page])
pg.run()

st.markdown('</div>', unsafe_allow_html = True)


if not st.session_state.show_nav:
    st.write("Navigation hidden. Click ☰ to show.")


st.set_page_config(page_title = "🚗 Car Sharing", page_icon = ":material/edit:")
