
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'Survey'
    players_per_group = None
    num_rounds = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass

def dcr_r(player):
    import random
    player.dcs_r = random.randint(1,2)
    # 1 for second round
    # 2 for last round

class Player(BasePlayer):
    dcs_initial = models.IntegerField(choices=[[1, 'Contract 1 (Deductible: 300)'], [2, 'Contract 2 (Deductible: 500)'], [3, 'Contract 3 (Deductible: 1000)'], [4, 'Contract 4 (Deductible: 1500)'], [5, 'Contract 5 (Deductible: 2000)'], [6, 'Contract 6 (Deductible: 2500)'], [7, 'Unsure']], label='Which option did you prefer? Please select one:', widget=widgets.RadioSelect)
    sure1 = models.IntegerField(choices=[[1, 'Yes'], [0, 'No']], label='Did you feel SURE about the best choice for you?', widget=widgets.RadioSelect)
    sure2 = models.IntegerField(choices=[[1, 'Yes'], [0, 'No']], label='Did you know the benefits and risks of each option?', widget=widgets.RadioSelect)
    sure3 = models.IntegerField(choices=[[1, 'Yes'], [0, 'No']], label='Were you clear about which benefits and risks matter most to you?', widget=widgets.RadioSelect)
    sure4 = models.IntegerField(choices=[[1, 'Yes'], [0, 'No']], label='Did you have enough support and advice to make a choice', widget=widgets.RadioSelect)
    ok1 = models.IntegerField(choices=[[0, 'Amount that you have to pay towards your treatment costs every year before the insurance company starts to pay out.'], [1, 'Monthly payment for health insurance.'], [2, '10 per cent of any treatment costs to be paid after deductible, up to 700 CHF. '], [3, 'Amount to be paid per day spent at the hospital.'], [4, "Don't know"]], label='Select the definition for health insurance premium that fits best:')
    ok3 = models.IntegerField(choices=[[0, 'Amount that you have to pay towards your treatment costs every year before the insurance company starts to pay out.'], [1, 'Monthly payment for health insurance.'], [2, '10 per cent of any treatment costs to be paid after deductible, up to 700 CHF. '], [3, 'Amount to be paid per day spent at the hospital.'], [4, "Don't know"]], label='Select the definition for health insurance deductible that fits best:')
    ok2 = models.IntegerField(choices=[[0, '10 CHF'], [1, '15 CHF'], [2, '20 CHF'], [3, "Don't Know"]], label='The daily contribution to the costs of a hospital stay amounts to:')
    ok4 = models.IntegerField(choices=[[1, 'January'], [2, 'February'], [3, 'March'], [4, 'April'], [5, 'May'], [6, 'June'], [7, 'July'], [8, 'August'], [9, 'September'], [10, 'October'], [11, 'November'], [12, 'December'], [13, "Don't know"]], label='By the end of what month do you have to terminate your policy if you are changing plans?')
    ok5 = models.IntegerField(choices=[[0, 'Amount that you have to pay towards your treatment costs every year before the insurance company start to pay out.'], [1, 'Monthly payment for health insurance.'], [2, '10 per cent of any treatment costs to be paid after deductible, up to 700 CHF. '], [3, 'Amount to be paid per day spent at the hospital.'], [4, "Don't know"]], label='Select the definition for retention fee:')
    ok6 = models.IntegerField(choices=[[1, 'True'], [2, 'False'], [3, "Don't know"]],
                              label='Compulsory health insurance offers the same range of services and benefits to all insured people. ',
                              widget=widgets.RadioSelect)
    ok7 = models.IntegerField(choices=[[1, 'True'], [2, 'False'], [3, "Don't know"]],
                              label='For compulsory insurance, people are free to choose any insurer and type of insurance operating in their place of residence.',
                              widget=widgets.RadioSelect)
    ok8 = models.IntegerField(choices=[[1, 'True'], [2, 'False'], [3, "Don't know"]],
                              label='Insurance companies are obliged to offer you the desired supplementary cover.', widget=widgets.RadioSelect)
    ok9 = models.IntegerField(choices=[[1, 'True'], [2, 'False'], [3, "Don't know"]],
                              label='Supplementary insurance is a form of social security.', widget=widgets.RadioSelect)
    ok10 = models.IntegerField(choices=[[1, 'True'], [2, 'False'], [3, "Don't know"]],
                               label='Before you are offered supplementary insurance, the health insurance company will ask you to complete a health questionnaire.', widget=widgets.RadioSelect)
    dcs_r = models.IntegerField()
    lot1 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=100, min=0)
    lot2 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=100, min=0)
    lot3 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=100, min=0)
    lot4 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=10000,
                               min=0)
    lot5 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=100, min=0)
    lot6 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to play this lottery:', max=400, min=0)
    lot7 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to to avoid this lottery:', max=80,
                               min=0)
    lot8 = models.IntegerField(label='Maximum amount of CHF I am willing to pay to to avoid this lottery:', max=100,
                               min=0)
    lot9 = models.IntegerField(label='Minimum value of X (CHF) to make this lottery acceptable:', min=0)
    lot10 = models.IntegerField(label='Minimum value of X (CHF) to make this lottery acceptable:', min=0)
    general_risk = models.IntegerField(choices=[[0, ''], [1, ''], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, ''], [8, ''], [9, ''], [10, '']], widget=widgets.RadioSelect)
    age = models.IntegerField(label='Age:', max=100, min=10)
    gender = models.IntegerField(choices=[[1, 'Female'], [2, 'Male']], label='Gender:', widget=widgets.RadioSelectHorizontal)
    swiss = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='Are you Swiss?', widget=widgets.RadioSelectHorizontal)
    education = models.IntegerField(choices=[[1, 'Lower secondary school (Gymnasiums or Kantonsschule)'], [2, 'Upper secondary school (High school, Vocational education and training (VET), Baccalaureate, or Upper secondary specialized school)'], [3, 'Tertiary (University, Fachhochschule or Höhere Fachschule)'], [4, 'Masters'], [5, 'PhD']])
    canton = models.IntegerField(choices=[[1, 'Luzern (LU)'], [2, 'Zurich (ZH)'], [3, 'Bern (BE)'], [4, 'Uri (UR)'], [5, 'Schwyz  (SZ)'], [6, 'Obwalden (OW)'], [7, 'Nidwalden (NW)'], [8, 'Glarus (GL)'], [9, 'Zug (ZG)'], [10, 'Freiburg (FR)'], [11, 'Solothurn (SO)'], [12, 'Basel-Stadt (BS)'], [13, 'Basel-Landschaft (BL)'], [14, ' \tSchaffhausen (SH)'], [15, 'Appenzell Ausserrhoden (AR)'], [16, 'Appenzell Innerrhoden (AI)'], [17, 'St. Gallen (SG)'], [18, 'Graubünden (GR)'], [19, 'Aargau (AG)'], [20, 'Thurgau (TG)'], [21, 'Ticino (TI)'], [22, 'Vaud (VD)'], [23, 'Valais (VS)'], [24, 'Neuchâtel (NE)'], [25, 'Genève (GE)'], [26, 'Jura (JU)']], label='What canton do you live in?')
    study_area = models.IntegerField(choices=[[1, 'Natural and Physical Sciences'], [2, 'Information Technology'], [3, 'Engineering and related Technologies'], [4, 'Architecture and Building'], [5, 'Agriculture, Environmental and Related Studies'], [6, 'Health Sciences'], [7, 'Education'], [8, 'Business and Management'], [9, 'Psychology or Social work'], [10, 'Law'], [11, 'Economics'], [12, 'Communication'], [13, 'Hospitality'], [14, 'Other']])
    email = models.StringField(blank=True, label='Would you like to know about the results of this experiment or participate in future experiments? If so, please enter your e-mail:')
    civil_status = models.IntegerField(choices=[[1, 'Single'], [2, 'Married']], label='What is your civil status?', widget=widgets.RadioSelectHorizontal)
    household_size = models.IntegerField(label='Number of people living in your household:', max=40, min=1)
    workstat = models.IntegerField(choices=[[1, 'Studying'], [2, 'Employed'], [3, 'Self-employed'], [4, 'Unemployed']], label='What is your work status?')
    annual_income = models.IntegerField(choices=[[1, '< 12,000 CHF'], [2, '12,000 - 24,000 CHF'], [3, '24,001 - 36,000 CHF'], [4, '36,001 - 48,000 CHF'], [5, '48,001 - 60,000 CHF'], [6, '> 60,000 CHF']], label='What is your annual income?')
    health = models.StringField(choices=[['Very good', 'Very good'], ['Good', 'Good'], ['Fair', 'Fair'], ['Poor', 'Poor'], ['Very poor', 'Very poor']], label='In general, how would you describe your health status? ')
    doc = models.IntegerField(label='How many doctor visits have you had in the last 12 months?', max=99, min=0)
    switch = models.StringField(choices=[['Last year', 'Last year'], ['2 years ago', '2 years ago'], ['Longer than 2 years ago', 'More than 2 years ago'], ['Never', 'Never'], ["Don't know", "Don't know"]], label='When was the last time you switched or changed your health insurance?')
    ded = models.IntegerField(choices=[[300, '300'], [500, '500'], [1000, '1000'], [1500, '1500'], [2000, '2000'], [2500, '2500'], [0, "Don't know"]], label='What is your current deductible level?')
    supplementary = models.IntegerField(choices=[[1, 'Yes'], [2, 'No'], [3, "Don't know"]], label='Do you currently have supplementary or voluntary health insurance?')
    hil1 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='1. understand the concepts and terms about health insurances?', widget=widgets.RadioSelect)
    hil2 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='2. can estimate what you will have to pay for your care in the coming year (without emergencies)? ', widget=widgets.RadioSelect)
    hil3 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='3. know which questions to ask in order to choose the health insurance that is right for you? ', widget=widgets.RadioSelect)
    hil4 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='4. know where to find the information you need to choose a health insurance? ', widget=widgets.RadioSelect)
    hil5 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='5. know where to go for financial help if you cannot pay your health insurance? ', widget=widgets.RadioSelect)
    hil6 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='6. are choosing a health insurance that suits you?', widget=widgets.RadioSelect)
    hil7 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='7. can find out if an insurance policy covers unexpected costs, such as hospitalization? ', widget=widgets.RadioSelect)
    hil8 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='8. understand what you would have to pay for a visit to the emergency room? ', widget=widgets.RadioSelect)
    hil9 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='9. can find out how much you have to pay yourself for a visit to a medical specialist?', widget=widgets.RadioSelect)
    hil10 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='10. can find out how much you have to pay for medicine on prescription? ', widget=widgets.RadioSelect)
    hil11 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='11. can find out which doctors and hospitals are covered by an insurance policy?', widget=widgets.RadioSelect)
    hil12 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='12. can find out what the differences are between insurance policies? ', widget=widgets.RadioSelect)
    hil13 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='13. can find out if you have to pay for certain care yourself? ', widget=widgets.RadioSelect)
    hil14 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='14. know what to do if your health insurance company refuses to pay for care that you think should be reimbursed? ', widget=widgets.RadioSelect)
    hil15 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='15. can find out how much you have to pay out of your own pocket?', widget=widgets.RadioSelect)
    hil16 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='16. can find out how much of the costs your health insurance will reimburse? ', widget=widgets.RadioSelect)
    hil17 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='17. know which questions to ask your health insurance company if you have a problem with a reimbursement? ', widget=widgets.RadioSelect)
    hil18 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='18. will find out what is and is not covered by your health insurance before you receive certain care?', widget=widgets.RadioSelect)
    hil19 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='19. will contact customer service to ask what care is covered by your health insurance? ', widget=widgets.RadioSelect)
    hil20 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='20. can find out whether a doctor has a contract with your health insurer before you visit that doctor?', widget=widgets.RadioSelect)
    hil21 = models.IntegerField(choices=[[1, ''], [2, ''], [3, ''], [4, '']], label='21. look at the overviews of your health insurance to see what you still have to pay and what the health insurance company has reimbursed?', widget=widgets.RadioSelect)

class Risk_Attitudes(Page):
    form_model = 'player'
    form_fields = ['lot1', 'lot2', 'lot3', 'lot4', 'lot5', 'lot6', 'lot7', 'lot8', 'lot9', 'lot10', 'general_risk']
    @staticmethod
    def before_next_page(player, timeout_happened):
        dcr_r(player)
class DCS(Page):
    form_model = 'player'
    form_fields = ['dcs_initial', 'sure1', 'sure2', 'sure3', 'sure4']
class HIL(Page):
    form_model = 'player'
    form_fields = ['hil1', 'hil2', 'hil3', 'hil4', 'hil5', 'hil6', 'hil7', 'hil8', 'hil9', 'hil10', 'hil11', 'hil12', 'hil13', 'hil14', 'hil15', 'hil16', 'hil17', 'hil18', 'hil19', 'hil20', 'hil21']
class Objective_HIL(Page):
    form_model = 'player'
    form_fields = ['ok1', 'ok2', 'ok3', 'ok4', 'ok5', 'ok6', 'ok7', 'ok8', 'ok9', 'ok10']
class General_Info(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'swiss', 'education', 'canton', 'study_area', 'civil_status', 'household_size', 'workstat', 'annual_income', 'health', 'doc', 'switch', 'ded', 'supplementary']
class Thanks(Page):
    form_model = 'player'
    form_fields = ['email']

page_sequence = [Risk_Attitudes, DCS, HIL, Objective_HIL, General_Info, Thanks]