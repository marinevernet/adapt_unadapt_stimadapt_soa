import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import os
from datetime import datetime

# MUST be the first Streamlit command in your script
st.set_page_config(layout="wide")

# 1. INITIALIZATION & SESSION STATE
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = ""
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# 2. THE CONTENT HUB
computer = "Romaric"

if computer == "Romaric":
    path_save = "C:/Users/Romar/Documents/PhD_Agency/Code/script/Script_stim_adapt"

# List of questionnaires name for saving    
# AABS: Adaptive Agency Beliefs Scale (named LoCSoA when the data were collected)
list_of_questionnaires = ["AABS", "BIS", "AMI", "EHI"]

# Every questionnaire has its own specific options and mappings
CONTENT = {
    # ENGLISH VERSION
    "English": {
        "setup_title": "Participant Registration",
        
        "next": "Next",
        "finish": "Finish",
        
        # Questionnaire 1: AABS (Adaptive Agency Beliefs Scale) 
        "q1_title": "Questionnaire 1/4",
        "q1_instr": "You will be presented with a number of statements. \n Please think carefully about each statement and determine to what extent you agree or disagree with it. \n Judge the statements by referring to your overall feelings and/or beliefs. \n We understand that it will sometimes be difficult to choose a single answer, as most statements depend on the context. \n Nevertheless, please choose the answer that best corresponds to your feelings and beliefs.",      
        "q1_opts": ["Strongly Disagree", "Disagree", "Slightly Disagree", "Slightly Agree", "Agree", "Strongly Agree"],
        "q1_qs": [  "Seeing the bright side of things is very easy for me",
                    "I don't like having to tell people what to do",
                    "People's support has a positive impact on my life",
                    "I like to be surprised by events in my daily life",
                    "Our world has basic or ingrained dispositions, and you can't really do much to change them",
                    "No matter what kind of person someone is, they can always change very much",
                    "I have difficulty sticking to my goals",
                    "I feel that I have a number of good qualities",					
                    "People can learn new things, but how intelligent they are stays pretty much the same",	
                    "I feel happy with myself as a person",	
                    "When the world changes, people can feel confused",
                    "I take a positive attitude toward myself",						
                    "I am more likely to do things quickly rather than carefully",
                    "In general, I feel that people treat me well",						
                    "I say things without thinking",						
                    "People can always change their personality",						
                    "I feel more comfortable when things are not too strictly organized",				
                    "I enjoy taking challenges",						
                    "I would do better in life if people did not make things hard for me",					
                    "In a group, I like to take charge and make decisions",					
                    "I look upon potential disappointments in life as opportunities to improve and grow as a person",					
                    "People often just use me instead of treating me as a person",					
                    "The world is ever changing and you can have some influence on it",					
                    "Someone's personality is a part of them that they can't change very much",						
                    "Although I hate to admit it, I'd like to be successful without having to work hard on it",				
                    "Everyone can change even their basic intelligence level considerably",					
                    "At times I think I am no good at all",						
                    "Society can grow and evolve, if people take actions in it",					
                    "The society evolves too fast for people to adapt",					
                    "I always think twice before speaking",						
                    "I see no point in spending time on a task that is probably too difficult",				
                    "I am very good at influencing people",						
                    "People can always substantially change how intelligent they are",					
                    "I'm having trouble finding life enjoyable",						
                    "I am willing to put effort when something is worth it",				
                    "I am not interested in being a leader",						
                    "It's much more important for me to learn things than it is to get the best result",				
                    "Everyone has a certain amount of intelligence, and we can not really do much to change it",					
                    "When the world evolves it offers new opportunities to people",				
                    "I wish I could have more respect for myself",						
                    "I plan and organize my schedule in detail",						
                    "People can't really change what kind of personality they have",				
                    "People always have the possibility to fit in an evolving society",						
                    "If I knew I wasn't going to do well at a task, I probably wouldn't do it even if I might learn a lot from it",					
                    "I am able to work effectively toward a long-term goal",				
                    "Some societal trends may dominate for a while, but the fundamental nature of our world is something that cannot be changed much",				
                    "People say that I am well organized (that I do things in a systematic manner)",						
                    "I'm usually not happy with myself"],
        
        # Questionnaire 2: BIS
        "q2_title": "Questionnaire 2/4",
        "q2_instr": "People act and think differently in various situations. This questionnaire aims to evaluate some of your ways of acting and thinking. \n Judge the statements by referring to your general feeling and/or your beliefs. Answer quickly and honestly.",
        "q2_opts": ["Rarely/Never", "Occasionally", "Often", "Almost Always/Always"],
        "q2_qs": [" I plan tasks carefully",
            "I do things without thinking",
            "I make up my mind quickly",
            "I am happy-go-lucky",
            "I don't 'pay attention'",
            "I have 'racing' thoughts",
            "I plan trips well ahead of time",
            "I am self-controlled",
            "I concentrate easily",
            "I save regularly",
            "I squirm at plays or lectures",
            "I am a careful thinker",
            "I plan for job security",
            "I say things without thinking",
            "I like to think about complex problems",
            "I change jobs",
            "I act 'on impulse'",
            "I get easily bored when solving thought problems",
            "I act on the spur of the moment",
            "I am a steady thinker",
            "I change residences",
            "I buy things on impulse",
            "I can only think about one thing at a time",
            "I change hobbies",
            "I spend or charge more than I earn",
            "I often  have extraneous thoughts when thinking",
            "I am more interested in the present than in the future",
            "I am restless at the theater or lectures",
            "I like puzzles",
            "I am future oriented" ],
        
        # Questionnaire 3: AMI
        "q3_title": "Questionnaire 3/4",
        "q3_instr": "You will be presented with a number of statements. \n Please think carefully about each statement and determine to what extent you agree or disagree with it. \n Please call the experimenter if you have any questions. In the past 2 weeks...",
        "q3_opts": ["Completely untrue", "Mostly untrue", "Neither true nor untrue", "Quite true", "Completely true"],
        "q3_qs":   ["I feel sad or upset when I hear bad news",
                    "I start conversations with random people",
                    "I enjoy doing things with people I have just met",
                    "I suggest activities for me and my friends to do",
                    "I make decisions firmly and without hesitation",
                    "After making a decision, I will wonder if I have made the wrong choice" ,
                    "Based on the last two weeks, I would say I care deeply about how my loved ones think of me",
                    "I go out with friends on a weekly basis",
                    "When I decide to do something, I am able to make an effort easily",
                    "I don't like to laze around",
                    "I get things done when they need to be done, without requiring reminders from others",
                    "When I decide to do something, I am motivated to see it through to the end",
                    "I feel awful if I say something insensitive",
                    "I start conversations without being prompted",
                    "When I have something I need to do, I do it straightaway so it is out of the way",
                    "I feel bad when I hear an acquaintance has an accident or illness",
                    "I enjoy choosing what to do from a range of activities",
                    "If I realise I have been unpleasant to someone, I will feel terribly guilty afterwards"],
        
        # Questionnaire 4: EHI
        "q4_title": "Questionnaire 4/4",
        "q4_instr": "Please indicate your hand preference for each of the activities below. If the preference is so strong that you only use the other hand if you are absolutely forced to, select 'only left hand / only right hand'.",
        "q4_opts": ["Only left hand", "Left hand", "Left or right hand", "Right hand", "Only right hand"],
        "q4_qs": ["WRITING", "DRAWING", "THROWING", "SCISSORS", 
                  "TOOTHBRUSH", "KNIFE (WITHOUT FORK)",
                  "SPOON", "BROOM (UPPER HAND)",
                  "STRIKING MATCH (MATCH)",
                  "OPENING BOX (LID)"]
    },
    
    # FRENCH VERSION
    "Français": {
        "setup_title": "Enregistrement du participant",
        
        "next": "Suivant",
        "finish": "Terminer",
        
        # Questionnaire 1: AABS (Adaptive Agency Beliefs Scale) 
        "q1_title": "Questionnaire 1/4",
        "q1_instr": "Il vous sera présenté un certain nombre d'affirmations. \n Réfléchissez bien à chaque affirmation et déterminez dans quelle mesure vous êtes d'accord ou non avec elle. \n Jugez les affirmations en vous référant à votre sentiment général et/ou à vos convictions. \n Nous comprenons qu'il sera parfois difficile de choisir une seule réponse, car la plupart des affirmations dépendent du contexte. \n Néanmoins, veuillez choisir la réponse qui correspond le mieux à vos sentiments et à vos convictions.",      
        "q1_opts": ["Pas du tout d'accord", "Pas d'accord", "Plutôt pas d'accord", "Plutôt d'accord", "D'accord", "Tout à fait d'accord"],
        "q1_qs": [  "Il m'est très facile de voir le bon côté des choses",
                    "Je n'aime pas avoir à dire aux autres ce qu'ils doivent faire",
                    "Le soutien que des personnes peuvent m'apporter a un impact positif sur ma vie",
                    "J'aime être surpris(e) par les événements de ma vie quotidienne",
                    "Notre monde a des dispositions fondamentales ou enracinées, et il est difficile de les changer",
                    "Peu importe le type de personne que quelqu'un est, il peut toujours beaucoup changer",
                    "J'ai du mal à me tenir à mes objectifs",
                    "Je pense que je possède un certain nombre de belles qualités",					
                    "Les gens peuvent apprendre de nouvelles choses, mais leur intelligence reste la même",	
                    "Je me sens heureux/heureuse avec moi-même en tant que personne",	
                    "Lorsque le monde change, les gens peuvent se sentir désorientés",
                    "J'ai une attitude positive envers moi-même",						
                    "A choisir, je suis plus enclin(e) à faire les choses rapidement qu'avec précaution",
                    "En général, j'ai l'impression que les gens me traitent bien",						
                    "Je dis des choses sans réfléchir",						
                    "Les gens peuvent toujours changer leur personnalité",						
                    "Je me sens plus à l'aise lorsque les choses ne sont pas trop strictement organisées",				
                    "J'aime relever des défis",						
                    "Je réussirais mieux dans la vie si les gens ne me compliquaient pas la tâche",					
                    "Dans un groupe, j'aime prendre des responsabilités et des décisions",					
                    "Je considère les possibles échecs dans la vie comme des occasions pour m'améliorer et mûrir en tant que personne",					
                    "Les gens se contentent souvent de m'utiliser au lieu de me traiter comme une personne",					
                    "Le monde est en constante évolution et nous pouvons avoir une influence sur lui",					
                    "La personnalité fait partie intégrante d'une personne et elle ne peut pas vraiment la changer",						
                    "Même si je n'aime pas l'admettre, j'aimerais avoir du succès sans avoir à travailler dur",				
                    "Chacun peut largement modifier son niveau d'intelligence de base",					
                    "Parfois, je me sens vraiment inutile",						
                    "La société peut se développer et évoluer, si les gens agissent en son sein",					
                    "La société évolue trop vite pour que les gens puissent s'y adapter",					
                    "Je réfléchis toujours à deux fois avant de parler",						
                    "Je ne vois pas l'intérêt de consacrer du temps à une tâche qui est probablement trop difficile",				
                    "Je suis très doué(e) pour influencer les gens",						
                    "Les gens peuvent toujours changer fortement leur niveau d'intelligence",					
                    "J'ai du mal à trouver la vie agréable",						
                    "Je suis prêt(e) à faire des efforts lorsque quelque chose en vaut la peine",				
                    "Je ne suis pas intéressé(e) par le rôle de leader",						
                    "Il est beaucoup plus important pour moi d'apprendre des choses que d'obtenir le meilleur résultat",				
                    "Tout le monde a un certain degré d'intelligence, et nous ne pouvons pas vraiment faire grand-chose pour le changer",					
                    "Lorsque le monde évolue, cela peut offrir de nouvelles opportunités aux personnes",				
                    "J'aimerais avoir plus de respect pour moi-même",						
                    "Je planifie et organise mon emploi du temps en détail",						
                    "Les gens ne peuvent pas vraiment changer le type de personnalité qu'ils ont",				
                    "Les gens ont toujours la possibilité de s'adapter dans une société en évolution",						
                    "Si je sais que je ne vais pas réussir quelque chose, je ne le fais probablement pas, même si j'aurais pu beaucoup apprendre",					
                    "Je suis capable de travailler efficacement pour atteindre un objectif à long terme",				
                    "Certaines tendances de la société peuvent dominer pendant un certain temps, mais la nature fondamentale de notre monde est quelque chose qui ne peut pas être beaucoup changé",				
                    "Les gens disent que je suis bien organisé(e)",						
                    "Je ne suis généralement pas satisfait(e) de moi-même"],
        
        # Questionnaire 2: BIS
        "q2_title": "Questionnaire 2/4",
        "q2_instr": "Les gens agissent et réfléchissent différemment devant des situations variées. Ce questionnaire a pour but d'évaluer certaines de vos façons d'agir et de réfléchir. \n Jugez les affirmations en vous référant à votre sentiment général et/ou à vos convictions. Répondez vite et honnêtement.",
        "q2_opts": ["Rarement/Jamais", "Occasionnellement", "Souvent", "Presque toujours"],
        "q2_qs": ["Je prépare soigneusement les tâches à accomplir",
            "Je fais les choses sans réfléchir",
            "Je me décide rapidement",
            "Je suis insouciant(e)",
            "Je ne fais pas attention",
            "Mes pensées défilent très vite",
            "Je programme mes voyages longtemps à l'avance",
            "Je suis maître.sse de moi",
            "Je me concentre facilement",
            "Je mets de l'argent de côté raisonnablement",
            "Je ne tiens pas en place aux spectacles ou aux conférences",
            "Je réfléchis soigneusement",
            "Je veille à ma sécurité d'emploi",
            "Je dis les choses sans réfléchir",
            "J'aime réfléchir à des problèmes complexes",
            "Je change d'emploi",
            "J'agis sur un 'coup de tête'",
            "Réfléchir sur un problème m'ennuie vite",
            "J'agis selon l'inspiration du moment",
            "Je réfléchis posément",
            "Je change de logement",
            "J'achète les choses sur un 'coup de tête'",
            "Je ne peux penser qu'à un problème à la fois",
            "Je change de loisir",
            "Je dépense ou paye à crédit plus que je ne gagne",
            "Lorsque je réfléchis d'autres pensées me viennent à l'esprit",
            "Je m'intéresse plus au présent qu'à l'avenir",
            "Je m'impatiente lors de conférences ou de discussions",
            "J'aime les 'casse-têtes'",
            "Je fais des projets pour l'avenir" ],
        
        # Questionnaire 3: AMI
        "q3_title": "Questionnaire 3/4",
        "q3_instr": "Il vous sera présenté un certain nombre d'affirmations. \n Réfléchissez bien à chaque affirmation et déterminez dans quelle mesure vous êtes d'accord ou non avec elle. \n Si vous avez la moindre question demandez à l'expérimentateur. Dans les 2 dernières semaines...",
        "q3_opts": ["Complètement faux", "Plutôt faux", "Ni vrai ni faux", "Plutôt vrai", "Complètement vrai"],
        "q3_qs":   ["Je me sens triste ou boulversé.e quand j'apprends des mauvaises nouvelles",
                    "J'engage facilement la conversation avec n'importe qui",
                    "J'aime bien faire des activités avec des personnes que je connais depuis peu",
                    "Je propose à mes amis des activités à faire ensemble",
                    "Je prends des décisions avec détermination et sans hésitation",
                    "Après avoir pris une décision, je me demande si j'ai fait le mauvais choix" ,
                    "Au cours des deux dernières semaines, je dirais que je me préoccupe beaucoup de ce que mes proches pensent de moi",
                    "Je sors avec des amis toutes les semaines",
                    "Quand je décide de faire quelque chose, je m'y mets facilement",
                    "Je n'aime pas paresser",
                    "Je fais les tâches quand elles doivent être faites, sans qu'on me le rappelle",
                    "Quand je décide de faire quelque chose, je suis motivé.e à le terminer",
                    "Je me sens vraiment mal si je dis quelque chose de blessant",
                    "J'initie la conversation spontanément",
                    "Si je dois faire quelque chose, je le fais immédiatement afin que ça soit réglé",
                    "J'ai de la peine lorsque j'apprends qu'une connaissance a eu un accident ou est tombée malade",
                    "J'aime avoir le choix parmi plusieurs activités",
                    "Si je me rends compte que j'ai été désagréable avec quelqu'un, je me sens terriblement coupable"],
        
        # Questionnaire 4: EHI
        "q4_title": "Questionnaire 4/4",
        "q4_instr": "Merci d'indiquer votre préférence manuelle pour chacune des activités ci-dessous. Si la préférence est si forte que vous n'utilisez l'autre main que si vous y êtes absolument forcé, sélectionnez 'uniquement main gauche / uniquement main droite'.",
        "q4_opts": ["Uniquement main gauche", "Main gauche", "Main gauche ou main droite", "Main droite", "Uniquement main droite"],
        "q4_qs": ["ECRIRE", "DESSINER", "LANCER", "DECOUPER AVEC DES CISEAUX", 
                  "SE BROSSER LES DENTS", "UTILISER UN COUTEAU (SANS FOURCHETTE)",
                  "UTILISER UNE CUILLERE", "BALAYER (LA MAIN DU HAUT)",
                  "FROTTER UNE ALLUMETTE (MAIN QUI TIENT L'ALLUMETTE)",
                  "OUVRIR UNE BOITE (MAIN SUR LE COUVERCLE)"]
    }
}

def save_data(responses, label, options_list):
    clean_id = str(st.session_state.participant_id).strip().replace(" ", "_")
    filename = f"{clean_id}_{label}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    
    path_save_participant = os.path.join(path_save, 'data', clean_id, 'questionnaires')
    if not os.path.exists(path_save_participant):
        os.makedirs(path_save_participant)
    
    path_files = os.path.join(path_save_participant, filename)
    
    # Build the full list of rows FIRST
    rows = []
    for q_idx, text_ans in responses.items():
        rows.append({
            "Participant_ID": st.session_state.participant_id,
            "Question_Num": q_idx + 1,
            "Text_Answer": text_ans,
            "Answer_Code": options_list.index(text_ans) + 1,
        })
    
    # Save the entire DataFrame at once
    # Using index=False ensures we don't get that "Unnamed: 0" column
    pd.DataFrame(rows).to_csv(path_files, index=False)


# 4. PAGE ROUTING
ui = CONTENT[st.session_state.lang]

# --- PAGE 0: REGISTRATION ---
if st.session_state.page == 0:
    st.title(ui["setup_title"])
    st.session_state.lang = st.radio("Language / Langue", ["English", "Français"], horizontal=True)
    pid = st.text_input("Participant ID / ID du participant")
    if st.button("Start / Commencer"):
        if pid:
            st.session_state.participant_id = pid
            st.session_state.page = 1
            st.rerun()

# --- PAGE 1 & 2: RADIO (ONE ROW) ---
elif st.session_state.page in [1, 2]:
    
    p = st.session_state.page
    st.title(ui[f"q{p}_title"])
    st.info(ui[f"q{p}_instr"]) # UNIQUE INSTRUCTIONS HERE
    
    qs, opts = ui[f"q{p}_qs"], ui[f"q{p}_opts"]
    with st.form(f"f{p}"):
        res = {}
        for i, q in enumerate(qs):
            st.markdown(f"**{i+1}. {q}**")
            res[i] = st.radio(f"r{p}_{i}", opts, index=None, horizontal=True, label_visibility="collapsed")
                    
            st.write("---")
        # if st.form_submit_button(ui["next"]):
        #     if None in res.values(): st.warning("Please answer all questions.")
        #     else:
        #         name_questionnaire = list_of_questionnaires[p-1]
        #         save_data(res, f"questionnaire_{name_questionnaire}", opts)
        #         st.session_state.page += 1
        #         st.rerun()
        if st.form_submit_button(ui["next"]):
            if None in res.values(): 
                st.warning("Please answer all questions.")
            else:
                name_questionnaire = list_of_questionnaires[p-1]
                
                # This call now handles the entire CSV creation in one shot
                save_data(res, f"questionnaire_{name_questionnaire}", opts)
                
                st.session_state.page += 1
                st.rerun()
        
        
# --- PAGE 3 & 4: RADIO BUTTONS ---
elif st.session_state.page in [3, 4]:

    p = st.session_state.page
    st.title(ui[f"q{p}_title"])
    st.info(ui[f"q{p}_instr"]) 
    
    qs, opts = ui[f"q{p}_qs"], ui[f"q{p}_opts"]
    
    with st.form(f"f{p}"):
        res = {}
        for i, q in enumerate(qs):
            st.markdown(f"**{i+1}. {q}**")
            
            res[i] = st.radio(f"r{p}_{i}", opts, index=None, horizontal=True, label_visibility="collapsed")
            
            st.write("---")
            
        btn_text = ui["finish"] if p == 4 else ui["next"]
        
        # if st.form_submit_button(btn_text):
        #     # Check if all questions are answered (since index=None)
        #     if None in res.values():
        #         st.warning("Please answer all questions / Veuillez répondre à toutes les questions.")
        #     else:
        #         name_questionnaire = list_of_questionnaires[p-1]
        #         save_data(res, f"questionnaire_{name_questionnaire}", opts)
        #         st.session_state.page += 1
        #         st.rerun()
        if st.form_submit_button(btn_text):
            if None in res.values(): 
                st.warning("Please answer all questions / Veuillez répondre à toutes les questions.")
            else:
                name_questionnaire = list_of_questionnaires[p-1]
                # This call now handles the entire CSV creation in one shot
                save_data(res, f"questionnaire_{name_questionnaire}", opts)
                st.session_state.page += 1
                st.rerun()
                
# # --- PAGE 3 & 4: LIKERT SLIDERS ---
# elif st.session_state.page in [3, 4]:
#     p = st.session_state.page
#     st.title(ui[f"q{p}_title"])
#     st.info(ui[f"q{p}_instr"]) # UNIQUE INSTRUCTIONS HERE
    
#     qs, opts = ui[f"q{p}_qs"], ui[f"q{p}_opts"]
#     with st.form(f"f{p}"):
#         res = {}
#         for i, q in enumerate(qs):
#             st.markdown(f"**{i+1}. {q}**")
#             res[i] = st.select_slider(f"s{p}_{i}", options=opts, value=opts[len(opts)//2], label_visibility="collapsed")
#             st.write("---")
#         btn = ui["finish"] if p == 4 else ui["next"]
#         if st.form_submit_button(btn):
#             name_questionnaire = list_of_questionnaires[p-1]
#             save_data(res, f"questionnaire_{name_questionnaire}", opts)
#             st.session_state.page += 1
#             st.rerun()

# --- PAGE 5: SUCCESS ---
elif st.session_state.page == 5:
    st.balloons()
    st.success("All data saved! / Données enregistrées !")
    if st.button("Restart / Recommencer"):
        st.session_state.clear()
        st.rerun()




