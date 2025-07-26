
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="VarroaCtrl", layout="centered")
st.title("🐝 VarroaCtrl by Papavlachopoulos I.")

brood_frames = st.number_input("Πλαίσια σφραγισμένου γόνου:", min_value=0.0)
brood_coverage = st.slider("% κάλυψης γόνου:", 0.0, 100.0, 100.0)
p_phoretic = st.number_input("Φορετικό % προσβολής:", min_value=0.0)
population_frames = st.number_input("Πλαίσια πληθυσμού:", min_value=0.0)
date_str = st.text_input("Ημερομηνία (ΗΗ/ΜΜ/ΕΕΕΕ):", datetime.now().strftime("%d/%m/%Y"))

def get_k_factor(date_str):
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
        month = date.month
    except ValueError:
        return None
    if month in [1, 2]: return 1.5
    elif month in [3, 4]: return 2
    elif month in [5, 6, 7]: return 2.5
    else: return 3

if st.button("Υπολογισμός"):
    K = get_k_factor(date_str)
    if K is None:
        st.error("⚠ Λάθος μορφή ημερομηνίας.")
    else:
        cells_per_side = 3000
        brood_cells = brood_frames * cells_per_side * 2 * (brood_coverage / 100)
        bees = population_frames * 1580 * 1.2

        mites_brood = (K * brood_cells * p_phoretic) / 100
        mites_adult = (bees * p_phoretic) / 100
        total_mites = round(mites_brood + mites_adult)
        phoretic_mites = round(mites_adult)
        total_population = bees + brood_cells
        infestation_pct = 100 * (mites_brood + mites_adult) / total_population

        if brood_frames == 0:
            if p_phoretic <= 3:
                recommendation = "ΑΠΑΙΤΟΥΝΤΑΙ 2 εξαχνώσεις ανά 3 ημέρες."
            else:
                recommendation = "ΑΠΑΙΤΟΥΝΤΑΙ 3 εξαχνώσεις ανά 3 ημέρες."
        elif infestation_pct <= 1.9:
            recommendation = "ΑΠΑΙΤΕΙΤΑΙ 1 εξάχνωση."
        elif infestation_pct <= 2.9:
            recommendation = "ΑΠΑΙΤΕΙΤΑΙ ΚΥΚΛΟΣ εξαχνώσεων (6 εξαχνώσεις ανά 3 ημέρες) & μέτρηση με οινόπνευμα μετά από 15 ημέρες."
        else:
            recommendation = "ΑΠΑΙΤΕΙΤΑΙ ΚΥΚΛΟΣ εξαχνώσεων (6 εξαχνώσεις ανά 3 ημέρες) & μέτρηση με οινόπνευμα μετά από 15 ημέρες."

        st.success("**Συνολικό ποσοστό προσβολής βαρρόα:** {:.2f}%\n"
                   "**Φορετικές βαρρόα (ενήλικες):** {}\n"
                   "**Συνολικός εκτιμώμενος αριθμός βαρρόα:** {}\n\n"
                   "👉 **Σύσταση:** {}".format(infestation_pct, phoretic_mites, total_mites, recommendation))
