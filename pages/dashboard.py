import streamlit as st
from utils.db_connector import get_db
import plotly.graph_objects as go

def display_player_profile(athlete_name):
    db = get_db()
    athlete = db.athletes.find_one({"nome_da_atleta": athlete_name})
    
    if not athlete:
        st.error("Athlete data not found!")
        return
    
    # Handle dominant side (membro_dom is now a direct string value)
    dominant_side = athlete.get('membro_dom', 'N/A')

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Name:** {athlete.get('nome_da_atleta', 'N/A')}")
            st.write(f"**Position:** {athlete.get('posição', 'N/A')}")
            st.write(f"**Dominant Side:** {dominant_side}")
        with col2:
            st.write(f"**Height:** {athlete.get('altura', 'N/A')} cm")
            st.write(f"**Weight:** {athlete.get('peso', 'N/A')} kg")
            st.write(f"**Age:** {athlete.get('idade', 'N/A')}")
        with col3:
            st.write(f"**Maturity Level:** {athlete.get('nivel_maturacional', 'N/A')}")

def calculate_fms_averages():
    db = get_db()
    # Get all athletes' FMS scores
    athletes = db.athletes.find({}, {
        'deep_squat': 1,
        'hurdle_step': 1,
        'inline_lunge': 1,
        'ts_push_up': 1,
        'rotary_stability': 1,
        'da_sm': 1,
        'nda_sm': 1,
        'da_lr': 1,
        'nda_lr': 1,
        '_id': 0
    })
    
    # Initialize sum and count
    total_scores = [0] * 9
    count = 0
    
    # Calculate totals
    for athlete in athletes:
        scores = [
            athlete.get('deep_squat', 0) or 0,
            athlete.get('hurdle_step', 0) or 0,
            athlete.get('inline_lunge', 0) or 0,
            athlete.get('ts_push_up', 0) or 0,
            athlete.get('rotary_stability', 0) or 0,
            athlete.get('da_sm', 0) or 0,
            athlete.get('nda_sm', 0) or 0,
            athlete.get('da_lr', 0) or 0,
            athlete.get('nda_lr', 0) or 0
        ]
        total_scores = [sum(x) for x in zip(total_scores, scores)]
        count += 1
    
    # Calculate averages
    if count > 0:
        return [score / count for score in total_scores]
    return [0] * 9  # Return zeros if no data


def display_test_results(athlete_name):
    db = get_db()
    athlete = db.athletes.find_one({"nome_da_atleta": athlete_name})
    
    if not athlete:
        st.error("Athlete data not found!")
        return
    
    # List of FMS test fields
    fms_fields = [
        'deep_squat', 'hurdle_step', 'inline_lunge', 
        'ts_push_up', 'rotary_stability',
        'da_sm', 'nda_sm', 'da_lr', 'nda_lr'
    ]
    
    # Check if any FMS tests exist for this athlete
    if not any(field in athlete for field in fms_fields):
        st.info("No FMS test results available for this athlete.")
        return
    
    # FMS test names for display
    fms_tests = [
        'Deep Squat', 'Hurdle Step', 'Inline Lunge', 
        'TS Push Up', 'Rotary Stability',
        'DA Shoulder Mobility', 'NDA Shoulder Mobility',
        'DA Leg Raise', 'NDA Leg Raise'
    ]
    
    #Player scores
    player_scores = [
        athlete.get('deep_squat', 0) or 0,
        athlete.get('hurdle_step', 0) or 0,
        athlete.get('inline_lunge', 0) or 0,
        athlete.get('ts_push_up', 0) or 0,
        athlete.get('rotary_stability', 0) or 0,
        athlete.get('da_sm', 0) or 0,
        athlete.get('nda_sm', 0) or 0,
        athlete.get('da_lr', 0) or 0,
        athlete.get('nda_lr', 0) or 0
    ]
    
    # Calculate average scores
    average_scores = calculate_fms_averages()
    
    # Create radar chart using plotly
    st.subheader("Functional Movement Screen (FMS) - Radar Chart")
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=player_scores,
        theta=fms_tests,
        fill='toself',
        name='Player Scores',
        line_color='darkblue',
        fillcolor='rgba(0, 0, 139, 0.2)'  # darkblue with 20% opacity
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=average_scores,
        theta=fms_tests,
        fill='toself',
        name='Average Scores',
        line_color='red',
        fillcolor='rgba(255, 0, 0, 0.2)'  # red with 20% opacity
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]  # FMS scores range from 0 to 3
            )),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def display_jump_metrics(athlete_name):
    db = get_db()
    athlete = db.athletes.find_one({"nome_da_atleta": athlete_name})
    
    if not athlete:
        st.error("Athlete data not found!")
        return
    
    # Jump metrics to display
    jumps = [
        ('squat_jump', 'Squat Jump', 'cm'),
        ('cm_jump', 'CM Jump', 'cm')
    ]
    
    # Check if any jump metrics exist
    if not any(field in athlete for field, _, _ in jumps):
        st.info("No jump metrics available for this athlete.")
        return
    
    # Calculate averages
    average_squat_jump = db.athletes.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$squat_jump"}}}
    ]).next()['avg']
    
    average_cm_jump = db.athletes.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$cm_jump"}}}
    ]).next()['avg']
    
    # Prepare data for bar chart
    jump_names = ['Squat Jump', 'CM Jump']
    player_scores = [
        athlete.get('squat_jump', 0),
        athlete.get('cm_jump', 0)
    ]
    average_scores = [average_squat_jump, average_cm_jump]
    
    # Create bar chart using plotly
    st.subheader("Jump Performance")
    
    fig = go.Figure()
    
    # Add player scores
    fig.add_trace(go.Bar(
        x=jump_names,
        y=player_scores,
        name='Player Scores',
        marker_color='darkblue'
    ))
    
    # Add average scores
    fig.add_trace(go.Bar(
        x=jump_names,
        y=average_scores,
        name='Average Scores',
        marker_color='red'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title='Jump Type',
        yaxis_title='Height (cm)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def calculate_test_averages(test_name):
    db = get_db()
    try:
        result = db.athletes.aggregate([
            {"$match": {test_name: {"$exists": True}}},
            {"$group": {"_id": None, "avg": {"$avg": f"${test_name}"}}}
        ]).next()
        return round(result['avg'], 2)  # Round to 2 decimal places
    except StopIteration:
        # No documents match the criteria
        return None
    except Exception as e:
        st.error(f"Error calculating averages: {str(e)}")
        return None
    
def display_performance_charts(athlete_name):
    db = get_db()
    athlete = db.athletes.find_one({"nome_da_atleta": athlete_name})
    
    if not athlete:
        st.error("Athlete data not found!")
        return
    
    # Performance tests to display
    tests = [
        ('v_10m_s', '10m Speed', 's'),
        ('v_30m_s', '30m Speed', 's'),
        ('t_test_s', 'T Test', 's'),
        ('1x_bronco_test_s', 'Bronco Test', 's'),
        ('beep_test_min', 'Beep Test', 'min')
    ]
    
    # Check if any performance metrics exist
    if not any(field in athlete for field, _, _ in tests):
        st.info("No performance test results available for this athlete.")
        return
    
    # Create charts for each test
    for test_field, test_name, unit in tests:
        if test_field in athlete:
            st.subheader(test_name)
            
            # Get player score and average
            player_score = athlete[test_field]
            average_score = calculate_test_averages(test_field)
            
            # Create bar chart
            if average_score is not None:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=['Player', 'Average'],
                    y=[player_score, average_score],
                    marker_color=['darkblue', 'red'],
                    text=[f"{player_score} {unit}", f"{average_score:.2f} {unit}"],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    showlegend=False,
                    yaxis_title=f'Time ({unit})',
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.metric(test_name, f"{player_score} {unit}")


def show():
    # Initialize session state
    if 'selected_athlete' not in st.session_state:
        st.session_state.selected_athlete = None

    # Title
    st.title("Athlete Performance Dashboard")

    @st.cache_data
    def get_athlete_names():
        db = get_db()
        athletes = db.athletes.find({}, {"nome_da_atleta": 1, "_id": 0})
        return sorted([a['nome_da_atleta'] for a in athletes])

    # Athlete selection
    athlete_names = get_athlete_names()
    
    if not athlete_names:
        st.warning("No athletes found in the database!")
        return
    
    selected_athlete = st.selectbox(
        "Select Athlete", 
        athlete_names,
        index=0
    )

    # Display components
    if selected_athlete:
        st.header("Player Profile")
        display_player_profile(selected_athlete)
        display_test_results(selected_athlete)
        display_jump_metrics(selected_athlete)
        display_performance_charts(selected_athlete)