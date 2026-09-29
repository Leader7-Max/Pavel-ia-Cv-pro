import streamlit as st

@st.dialog("☕ Soutenez Pavel IA CV Pro !")
def afficher_popup_don():
    st.write("Si cette application vous aide à créer votre CV, vous pouvez soutenir le projet avec un petit don !")
    
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <a href="https://www.paypal.me/Pavelia38" target="_blank" style="text-decoration: none;">
                <img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_200x51.png" 
                     alt="PayPal Logo" style="max-width: 180px; margin-bottom: 15px;"><br>
                <span style="background-color: #0070BA; color: white; padding: 10px 20px; border-radius: 25px; font-weight: bold; font-size: 16px;">
                    💳 Faire un don via PayPal
                </span>
            </a>
        </div>
        <hr style="margin: 20px 0;">
        <p style="text-align: center; font-size: 14px;">
            📱 <b>Mobile Money / Contact :</b> +33 6 51 35 29 52
        </p>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("Continuer vers l'application", use_container_width=True):
        st.rerun()

def initialiser_systeme_don():
    # Affichage automatique au premier chargement
    if "popup_don_affiche" not in st.session_state:
        st.session_state.popup_don_affiche = True
        afficher_popup_don()

    # Bouton manuel dans la barre latérale
    with st.sidebar:
        if st.button("💖 Faire un don", use_container_width=True):
            afficher_popup_don()
