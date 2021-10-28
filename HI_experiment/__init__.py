
from otree.api import *
c = cu

doc = ''
class Constants(BaseConstants):
    name_in_url = 'HI_experiment'
    players_per_group = 1
    num_rounds = 12
    deductibles = (300, 500, 1000, 1500, 2000, 2500)
    #no minor, a, b, major, no major
    health_events = ('No', 'A', 'B', 'Yes', 'No')
    he_probs = (45, 32, 23, 9)
    premiums = (4900, 4800, 4500, 4200, 3800, 3500)
    he_costs = (0, 250, 1300, 3000)
    initial_balance = 500
    income = 5200
    timeout = 2
    payoff = cu(0)
    points_per_chf = 200
    plans = (1, 2, 3, 4, 5, 6)
    aging_round = 8
    he_probs2 = (10, 50, 40, 26)
    info_rounds = (3, 8)
    points_per_question = 10
    c_periods = 2
    instructions_template = 'HI_experiment/instructions.html'
    show_fee = 10

def creating_session(subsession):
    pass
class Subsession(BaseSubsession):
    creating_session = creating_session

def creating_session(subsession: Subsession):
    import itertools
    import random
    t = [0, 1, 2, 3, 4]
    random.shuffle(t)
    colors = itertools.cycle(t)
    for player in subsession.get_players():
        player.color = next(colors)
    for p in subsession.get_players():
        stimuli = read_csv()
        for stim in stimuli:
            Question.create(player=p, **stim)
# TREATMENTS (colors):
    # 0: blue - control group
    # 1: red - unqualified info
    # 2: green - ui and numerical info for purchase
    # 3: yellow - ui and graphical info for purchase
    # 4: orange - ui and 2 types of info for purchase

class Group(BaseGroup):
    pass
def period_events(player):
    #method to determine randomly which health event will take place, 4 events in total (weighted)
    import random
    if player.round_number < Constants.aging_round:
        probs = Constants.he_probs
    else:
        probs = Constants.he_probs2
    
    a = probs[0]
    b = a + probs[1]
    minor = random.randint(0,100)
    major = random.randint(0,100)
    
    if minor <= a:
        player.hab = 0
    elif minor > a and minor <= b:
        player.hab = 1
    elif minor > b:
        player.hab = 2
    
    if major <= probs[3]:
        player.c_current = True
    else:
        player.c_current = False
    
def oop_payment(player):
    if player.he_cost >= player.deductible:
        oop = player.deductible
    else:
        oop = player.he_cost
    return oop
def total_balance(player):
    newbalance = player.balance + player.extra + Constants.income - player.premium - player.oop
    return newbalance
def calculate_payoff(player):
    participant = player.participant
    import math
    points = float(player.newbalance)
    convertion = float(Constants.points_per_chf)
    player.payoff = math.ceil(points / convertion)
    player.totalpayoff = int(player.payoff + Constants.show_fee)

def hi_table_costs(player):
    costs = []
    for cost in Constants.he_costs:
        for deductible in Constants.deductibles:
            if cost < deductible:
                costs.append(cost)
            else:
                costs.append(deductible)
    return costs
def current_contract_costs(player):
    plan_costs = []
    for cost in Constants.he_costs:
        if cost < player.deductible:
            plan_costs.append(cost)
        else:
            plan_costs.append(player.deductible)
    return plan_costs

    
def current_rp(player):
    if player.round_number < Constants.aging_round:
        current_risk_profile = Constants.he_probs
        player.rp = 1
    else:
        current_risk_profile = Constants.he_probs2
        player.rp = 2
    return current_risk_profile


def best_plan_calculator(player):
    current_rp(player)
    if player.rp < 2:
        probs = [i/100 for i in Constants.he_probs]
    else:
        probs = [i/100 for i in Constants.he_probs2]
    
    
    expected_costs_allplans = []
    #event cost per plan:
    for plan in Constants.plans:
        plan_costs = []
        p = plan -1
        for cost in Constants.he_costs:
            if cost < Constants.deductibles[p]:
                plan_costs.append(cost)
            else:
                plan_costs.append(Constants.deductibles[p])
        plan_ecosts = []
        i = 0
        for prob in probs:
            a = prob * plan_costs[i]
            plan_ecosts.append(a)
            i = i+1
        plan_he_cost = sum(plan_ecosts)
        if Constants.c_periods > 1:
            plan_he_cost = plan_he_cost + (Constants.c_periods - 1)*plan_ecosts[3]
        total_plan_ec = Constants.premiums[p] + plan_he_cost
        expected_costs_allplans.append(total_plan_ec)
    
    
    ######################################
    
    #determine best plan
    player.expected_cost_best_plan = int(min(expected_costs_allplans))
    #player.best_plan = Constants.plans.index(player.expected_cost_best_plan)
    player.best_plan = Constants.plans[expected_costs_allplans.index(player.expected_cost_best_plan)]
    
    #current expected total costs
    player_p = player.plan - 1
    player.cexp_tot_costs = int(expected_costs_allplans[player_p])
    
    # expected costs for all plans
    player.ec_1 = int(expected_costs_allplans[0])
    player.ec_2 = int(expected_costs_allplans[1])
    player.ec_3 = int(expected_costs_allplans[2])
    player.ec_4 = int(expected_costs_allplans[3])
    player.ec_5 = int(expected_costs_allplans[4])
    player.ec_6 = int(expected_costs_allplans[5])
    
    # max potential savings
    if player.expected_cost_best_plan < player.cexp_tot_costs:
        player.potential_savings = player.cexp_tot_costs - player.expected_cost_best_plan
    else:
        player.potential_savings = 0
def get_image_path(player):
    if player.rp ==1:
        return("hiexperiment/rp1_plan_comparison.png")
    elif player.rp == 2:
        return("hiexperiment/rp2_plan_comparison.png")
    
def read_csv():
    import csv
    import random

    f = open("stimuli.csv", encoding="utf-8-sig")
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
    return rows

def get_current_trial(player):
    pass


def expected_he_costs(player):
    current_rp(player)
    if player.rp == 1:
        probs = [i/100 for i in Constants.he_probs]
    else:
        probs = [i/100 for i in Constants.he_probs2]
    
    prob_x_cost = [a * b for a, b in zip(probs, Constants.he_costs)]
    if Constants.c_periods > 1:
        c_p = Constants.c_periods -1 
        he_ec = int(sum(prob_x_cost) + ( c_p * prob_x_cost[3] ))
        player.heonly_expected_costs = he_ec 
        return he_ec
    else:
        he_ec = int(sum(prob_x_cost))
        player.heonly_expected_costs = he_ec 
        return he_ec
def period_he_costs(player):
    #CURRENTLY WORKS WHEN PERIODS AFFECTED BY C ARE 2, IF CHANGED TO 2 MUST BE ADAPTED
    
    #current period costs for event c
    if player.c_current:
        c_curr = Constants.he_costs[3]
    else:
        c_curr = 0
    
    # previous period costs for event c
    if player.round_number == 1:
        player.c_previous = False
        c_lag1 = 0
    elif not player.in_round(player.round_number - 1).c_current:
        player.c_previous = False
        c_lag1 = 0
    elif player.in_round(player.round_number - 1).c_current:
        player.c_previous = True
        c_lag1 = Constants.he_costs[3]
    
    # total health event costs for period 
    player.he_cost = Constants.he_costs[player.hab] + c_curr + c_lag1

def wtp_order(player):
    import random
    player.wtp_o = random.randint(1,2)
    # 1 first graphical information and then numerical
    # 2 first numerical and then graphical

class Player(BasePlayer):
    consent = models.BooleanField()
    deductible = models.IntegerField(label='')
    premium = models.IntegerField()
    balance = models.IntegerField()
    extra = models.IntegerField(initial=0)
    selected_hi = models.IntegerField(blank=True, choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, '6']])
    selected_ded = models.IntegerField(blank=True)
    selected_premium = models.IntegerField(blank=True)
    hab = models.IntegerField()
    he_cost = models.IntegerField()
    oop = models.IntegerField()
    newbalance = models.IntegerField()
    change_hi = models.BooleanField(initial=False)
    plan = models.IntegerField()
    activechoiceafterhe = models.BooleanField()
    activehiselection = models.BooleanField(initial=False)
    correct_quiz = models.IntegerField(initial=0)
    round_qs = models.IntegerField(initial=0)
    total_qs_answered = models.IntegerField()
    color = models.IntegerField()
    rp = models.IntegerField()
    best_plan = models.IntegerField()
    cexp_tot_costs = models.IntegerField()
    potential_savings = models.IntegerField()
    expected_cost_best_plan = models.IntegerField()
    view_info = models.IntegerField(choices=[[0, '0'], [1, '1'], [2, '2']], initial=0)
    ec_1 = models.IntegerField()
    ec_2 = models.IntegerField()
    ec_3 = models.IntegerField()
    ec_4 = models.IntegerField()
    ec_5 = models.IntegerField()
    ec_6 = models.IntegerField()
    he_page_form = models.IntegerField(choices=[[-1, '-1'], [0, '0'], [1, '1'], [2, '2']])
    change_after_info = models.BooleanField(initial=False)
    heonly_expected_costs = models.IntegerField()
    c_current = models.BooleanField()
    c_previous = models.BooleanField()
    changed_hi_after_pinfo = models.BooleanField(initial=False)
    intro_review_1 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='1. Points can only be lost by paying my health insurance premium.', widget=widgets.RadioSelect)
    intro_review_2 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='2. I have to change my insurance contract in every period.', widget=widgets.RadioSelect)
    intro_review_3 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='3. Points are earned in every round by receiving a fixed income and correctly answering trivia questions.', widget=widgets.RadioSelect)
    intro_review_4 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='4. In every round, it is possible that a minor AND major health event occur. ', widget=widgets.RadioSelect)
    intro_review_5 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='5. My risk profile always stays the same. ', widget=widgets.RadioSelect)
    intro_review_6 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], label='6. The amount of points I earn during the experiment is converted into Swiss Francs at the end of the experiment. ', widget=widgets.RadioSelect)
    so_review = models.IntegerField(choices=[[51, '51%'], [32, '32%'], [67, '67%'], [14, '19%']],
                                    label='In this example, what is the probability that an event that costs 1300 points takes place?',
                                    widget=widgets.RadioSelect)
    he_review = models.StringField(
        choices=[['No major or minor event ', 'No major or minor event '], ['Yes, a major event', 'Yes, a major event'],
                 ['Only minor event A', 'Only minor event A']],
        label='In this example, did a health event take place in the previous round?', widget=widgets.RadioSelect)
    change_hi_review = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']],
                                           label='The time you spend on the page to change health insurance is subtracted from the time you have to answer trivia questions and get extra points.',
                                           widget=widgets.RadioSelect)
    wtp_g1 = models.BooleanField()
    wtp_g2 = models.BooleanField()
    wtp_g3 = models.BooleanField()
    wtp_p1 = models.BooleanField()
    wtp_p2 = models.BooleanField()
    wtp_p3 = models.BooleanField()
    wtp_p4 = models.BooleanField()
    wtp_p5 = models.BooleanField()
    wtp_p6 = models.BooleanField()
    wtp_o = models.IntegerField()
    period_events = period_events
    oop_payment = oop_payment
    total_balance = total_balance
    calculate_payoff = calculate_payoff
    hi_table_costs = hi_table_costs
    current_contract_costs = current_contract_costs
    current_rp = current_rp
    best_plan_calculator = best_plan_calculator
    get_image_path = get_image_path
    read_csv = read_csv
    get_current_trial = get_current_trial
    expected_he_costs = expected_he_costs
    period_he_costs = period_he_costs
    current_question = models.IntegerField(initial=0)
    totalpayoff = models.IntegerField()


class Welcome(Page):
    form_model = 'player'
    form_fields = ['consent']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        # Only shows this page if participant is in round 1
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player):
        return dict()

class Instructions_Review(Page):
    form_model = 'player'
    form_fields = ['intro_review_1', 'intro_review_2', 'intro_review_3', 'intro_review_4', 'intro_review_5', 'intro_review_6']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def error_message(player, values):
        correct = 0
        if values['intro_review_1'] == False:
            a1 = "1. Correct"
            correct += 1
        else: a1 = "1. Incorrect, you can also lose points due to adverse health events"
        
        if values['intro_review_2'] == False:
            a2 = "2. Correct"
            correct += 1
        else: a2 = "2. Incorrect, you don't have to change your insurance plan after every round"
        
        if values['intro_review_3'] == True:
            a3 = "3. Correct"
            correct += 1
        else: a3 = "3. Incorrect, you earn points by correctly answering trivia questions and your income"
        
        if values['intro_review_4'] == True:
            a4 = "4. Correct"
            correct += 1
        else: a4 = "4. Incorrect, both a minor and a major health event can take place in the same round"
        
        if values['intro_review_5'] == False:
            a5 = "5. Correct"
            correct += 1
        else: a5 = "5. Incorrect, your risk profile can change"
        
        if values['intro_review_6'] == True:
            a6 = "6. Correct"
            correct += 1
        else: a6 = "6. Incorrect, the points you have at the end of the experiment will be converted to CHF"
        
        if correct != 6:
            message = "Please select the correct answers below in order to proceed to the next screen:<br>" + a1 + "<br>" + a2 + "<br>" + a3 + "<br>" + a4 + "<br>" + a5 + "<br>" + a6
            return message
class Instructions_Status_Overview(Page):
    form_model = 'player'
    form_fields = ['so_review']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def error_message(player, values):
        if values['so_review'] != 67:
            return 'Your answer is incorrect, please select the correct answer to continue.'
class Instructions_Health_Event(Page):
    form_model = 'player'
    form_fields = ['he_review']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def error_message(player, values):
        if values['he_review'] != "Only minor event A":
            return 'Your answer is incorrect, please select the correct answer to continue.'
class Instructions_Change_HI(Page):
    form_model = 'player'
    form_fields = ['change_hi_review']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def error_message(player, values):
        if values['change_hi_review'] != True:
            return 'Your answer is incorrect, please select the correct answer to continue.'
class Start(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        ## user has 2 minutes to choose hi or get points - Modify in Constants (in minutes)
        participant.expiry = time.time() + Constants.timeout * 60
        participant.color = player.color


class Personalized_information(Page):
    form_model = 'player'
    form_fields = ['change_hi']
    @staticmethod
    def is_displayed(player):
        participant = player.participant
        if player.round_number == 1:
            return False
        elif participant.color == 0 or participant.color == 1:
            return False
        elif player.in_round(player.round_number - 1).view_info > 0:
            return True
        else:
            return False
    @staticmethod
    def vars_for_template(player):
        group = player.group
        participant = player.participant
         #1 blue - control group, distraction and no info
         #2 red - T1: distraction and unqualified info (graph)
         #3 green - T2: distraction, unqualified info, numerical/text info for cost
         #4 yellow - T3: distraction, unqualified info, graphical location for cost
         #5 orange - T4: distraction, unqualified info, numerical/text or graphical info for cost
        
        # generate list with expected costs for all plans:
        # use plan from previous round for information before HI selection
        player.plan = player.in_round(player.round_number - 1).plan
        best_plan_calculator(player)
        all_ec = [player.ec_1, player.ec_2, player.ec_3, player.ec_4, player.ec_5, player.ec_6]
        he_ec = player.expected_he_costs()
        
        # info type = 1 for numerical and = 2 for graphical 
        if participant.color == 2 and player.in_round(player.round_number - 1).view_info == 1 or participant.color == 4 and player.in_round(player.round_number - 1).view_info == 1:
            info_type = 1
            image_path = 0
        elif participant.color == 3 and player.in_round(player.round_number - 1).view_info == 1 or participant.color == 4 and player.in_round(player.round_number - 1).view_info == 2:
            info_type = 2
            image_path = player.get_image_path()
        
        # check if player has best plan and get best one 
        if player.best_plan == player.plan:
            have_best_plan = 1
            savings = 0
            better_plans = 0
            worse_plans = []
            extra_costs = []
            for ec in all_ec:
                if ec > player.cexp_tot_costs:
                    plan_extra_costs = ec - player.cexp_tot_costs
                    extra_costs.append(plan_extra_costs)
                    worse_plans.append(all_ec.index(ec) + 1)
        else:
            worse_plans = 0
            extra_costs = 0
            have_best_plan = 0
            savings = []
            better_plans = []
            for ec in all_ec:
                if ec < player.cexp_tot_costs:
                    plan_savings = player.cexp_tot_costs - ec
                    savings.append(plan_savings)
                    better_plans.append(all_ec.index(ec) + 1)
        
        
        return dict(
            have_best_plan = have_best_plan,
            info_type = info_type,
            savings = savings,
            better_plans = better_plans,
            image_path = image_path,
            worse_plans = worse_plans,
            extra_costs = extra_costs,
            he_ec = he_ec
        
        )
    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        import time
        return participant.expiry - time.time()

class Change_HI(Page):
    form_model = 'player'
    form_fields = ['selected_hi']
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            x = False
        elif player.in_round(player.round_number-1).change_hi == True:
            x = True
        elif player.change_hi == True:
            x = True
            player.change_after_info = True
        else:
            x = False 
        return x
        
    @staticmethod
    def vars_for_template(player):
        current_rp = player.current_rp()
        #costs = hi_table_costs(player)
        
        return dict(
        previous = player.in_round(player.round_number - 1).plan,
        he_event_0 = Constants.health_events[0],
        he_event_1 = Constants.health_events[1],
        he_event_2 = Constants.health_events[2],
        he_event_3 = Constants.health_events[3],
        he_event_4 = Constants.health_events[4],
        prob_h = current_rp[0],
        prob_a = current_rp[1],
        prob_b = current_rp[2],
        prob_c = current_rp[3],
        prob_noc = 100 - current_rp[3],
        he_cost_0 = Constants.he_costs[0],
        he_cost_1 = Constants.he_costs[1],
        he_cost_2 = Constants.he_costs[2],
        he_cost_3 = Constants.he_costs[3], 
        he_cost_4 = Constants.he_costs[0]
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.activehiselection = False
            player.selected_hi = None
            player.selected_ded = 0
            player.selected_premium = 0
        else:
            player.activehiselection = True
            i = player.selected_hi - 1
            player.selected_ded = Constants.deductibles[i]
            player.selected_premium = Constants.premiums[i]
        
        # setting variable to distinguish when changing after personalized info
        if player.in_round(player.round_number - 1).round_number in Constants.info_rounds and player.in_round(player.round_number - 1).view_info > 0:
            if player.activehiselection:
                player.changed_hi_after_pinfo = True
            else:
                player.changed_hi_after_pinfo = False
        
        #set change_hi back to False to avoid problems when selecting to change or not for next round 
        player.change_hi = False
    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        import time 
        return participant.expiry - time.time()

class Question(ExtraModel):
    player = models.Link(Player)
    question = models.StringField()
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    optionD = models.StringField()
    solution = models.IntegerField()
    choice = models.IntegerField()


def to_dict(question: Question, player: Player):
    return dict(
        question=question.question,
        optionA=question.optionA,
        optionB=question.optionB,
        optionC=question.optionC,
        optionD=question.optionD,
        correct_quiz=player.correct_quiz
    )


def get_question(player: Player, question_number: int):
    return Question.filter(player=player)[question_number]


def get_number_of_questions(player: Player):
    return len(Question.filter(player=player))

def assign_question_from_previous_round(player: Player):
    if player.round_number > 1:
        previous_round = player.round_number - 1
        previous_round_player = player.in_round(previous_round)
        print('(previous round) current question %d for round %d' % (previous_round_player.current_question, previous_round))
        player.current_question = previous_round_player.current_question
    else:
        player.current_question = 0

class Status_Overview(Page):
    form_model = 'player'


    @staticmethod
    def live_method(player: Player, data):

        print(data)
        print('current question %d for round %d' % (player.current_question, player.round_number))

        if 'init' in data:
            assign_question_from_previous_round(player)
            first_question_id = player.current_question
            first_question = get_question(player, first_question_id)
            response = dict(id_in_group=player.id_in_group, data=to_dict(first_question, player))
            return {0: response}
        elif 'answer' in data:
            answered_question_id = player.current_question
            answered_question = get_question(player, answered_question_id)
            player.total_qs_answered += 1
            player.round_qs += 1

            # Here I get answer of the player
            answered_question.choice = data['answer']
            if answered_question.choice == answered_question.solution:
                player.correct_quiz += 1

            if player.current_question < get_number_of_questions(player) - 1:
                player.current_question += 1
            else:
                player.current_question = 0

            next_question_id = player.current_question
            next_question = get_question(player, next_question_id)
            print('answered: %s' % answered_question)
            print('next: %s' % next_question)
            response = dict(id_in_group=player.id_in_group, data=to_dict(next_question, player))
            return {0: response}


    @staticmethod
    def is_displayed(player):
        return True
    @staticmethod
    def vars_for_template(player):
        # Getting rp in case previous page was skipped
        current_rp = player.current_rp()

        # player.extra = REPLACE ONCE IMPLEMENTED
        extra = player.extra

        # Variable definition for first round only
        if player.round_number == 1:
            # First round everyone has deductible of 300 and premium of 3700
            player.deductible = Constants.deductibles[0]
            player.premium = Constants.premiums[0]
            player.plan = 1
            # Initial balance set to 500 in constants
            player.balance = Constants.initial_balance
            previous_hecosts = 0
            player.total_qs_answered = 0
            if player.round_qs == 0:
                player.total_qs_answered = 0
                #player.correct_quiz = 0
        
        else:
            # Variable definition for round 2 and onwards
            # Total balance after previous round
            #player.extra = 0
            previous_hecosts = player.in_round(player.round_number - 1).oop 
            player.balance = player.in_round(player.round_number - 1).newbalance
            player.total_qs_answered = player.in_round(player.round_number - 1).total_qs_answered



            #deductible and premiums   
            if player.activehiselection == True:
                player.deductible = player.selected_ded
                player.premium = player.selected_premium
                index = Constants.deductibles.index(player.deductible)
                player.plan = Constants.plans[index]
            else: 
                player.deductible = player.in_round(player.round_number - 1).deductible
                player.premium = player.in_round(player.round_number - 1).premium
                player.plan = player.in_round(player.round_number - 1).plan
        
        
        return dict(
            deductible = player.deductible,
            premium = player.premium,
            balance = player.balance,
            #change EXTRA once implemented
            extra = extra,
            previous_hecosts = previous_hecosts,
            income = Constants.income,
            he_event_0 = Constants.health_events[0],
            he_event_1 = Constants.health_events[1],
            he_event_2 = Constants.health_events[2],
            he_event_3 = Constants.health_events[3],
            he_event_4 = Constants.health_events[4],
            prob_h = current_rp[0],
            prob_a = current_rp[1],
            prob_b = current_rp[2],
            prob_c = current_rp[3],
            prob_noc = 100 - current_rp[3],
            he_cost_0 = Constants.he_costs[0],
            he_cost_1 = Constants.he_costs[1],
            he_cost_2 = Constants.he_costs[2],
            he_cost_3 = Constants.he_costs[3], 
            he_cost_4 = Constants.he_costs[0],
            q_number = player.total_qs_answered + 1
             )
    @staticmethod
    def before_next_page(player, timeout_happened):
        #calculate extra points
        player.extra = player.correct_quiz * Constants.points_per_question
        best_plan_calculator(player)
    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        import time
        return participant.expiry - time.time()
class Health_event(Page):
    form_model = 'player'
    form_fields = ['he_page_form']
    timeout_seconds = 75
    @staticmethod
    def vars_for_template(player):
        group = player.group
        participant = player.participant
        # Use method in player to define health events randomly
        period_events(player)
        # Info for display on page 
        minor_event = Constants.health_events[player.hab]
        if player.hab == 0:
            minor_img = "hiexperiment/n.jpg"
        elif player.hab == 1:
            minor_img = "hiexperiment/a.jpg"
        elif player.hab == 2:
            minor_img = "hiexperiment/b.jpg"

        if player.c_current == True:
            major_event = "Yes"
            major_img = "hiexperiment/y.jpg"
        else:
            major_event = "No"
            major_img = "hiexperiment/n.jpg"

        # Info to desplay regarding events of previous round
        if player.round_number == 1:
            prev_minor = "None"
            prev_major = "None"
        else:
            prev_minor = Constants.health_events[player.in_round(player.round_number - 1).hab]
            if player.in_round(player.round_number - 1 ).c_current == True:
                player.c_previous = True
                prev_major = "Yes"
            else:
                player.c_previous = False
                prev_major = "No"

        
        # Determine the overall cost of the health events that happened (including previous periods in case of C)
        period_he_costs(player)
        # Define out-of-pocket cost for the player based on current health insurance for this round using oop_payment method in player
        player.oop = player.oop_payment()
        # Get final account balance for this round
        player.newbalance = player.total_balance()
        # determine possible costs according to risk profile and current plan
        #plan_costs = player.current_contract_costs()
        current_rp = player.current_rp()
        if participant.color == 1 or participant.color == 2:
            info = 0
        elif player.round_number in Constants.info_rounds:
            info = 1
        else:
            info = 0
        
        
        # information for treatment groups:
        if player.round_number in Constants.info_rounds:
            if participant.color == 1:
                treat = 1 # only unqualified
            elif participant.color == 2 or participant.color == 3:
                treat = 2 # only numerical OR graphical
            elif participant.color == 4:
                treat = 3 # numerical OR graphical
            else: 
                treat = 0
        else:
            treat = 0

        #expected cost based on rp
        he_ec = player.expected_he_costs()

        return dict(
        minor_event = minor_event,
        major_event = major_event,
        prev_minor = prev_minor,
        prev_major = prev_major,
        he_cost = player.he_cost,
        oop = player.oop,
        deductible = player.deductible,
        premium = player.premium,
        previousbalance = player.balance,
        newbalance = player.newbalance,
        info = info,
        extrapoints = player.extra,
        eventh = Constants.health_events[0],
        eventa = Constants.health_events[1],
        eventb = Constants.health_events[2],
        eventc = Constants.health_events[3],
        noeventc = Constants.health_events[4],
        beforeaging = Constants.aging_round - 1,
        prob_h = current_rp[0],
        prob_a = current_rp[1],
        prob_b = current_rp[2],
        prob_c = current_rp[3],
        prob_noc = 100 - current_rp[3],
        prob_h2 = Constants.he_probs2[0],
        prob_a2 = Constants.he_probs2[1],
        prob_b2 = Constants.he_probs2[2],
        prob_c2 = Constants.he_probs2[3],
        prob_noc2 = 100 - Constants.he_probs2[3],
        cost_h = Constants.he_costs[0],
        cost_a = Constants.he_costs[1],
        cost_b = Constants.he_costs[2],
        cost_c = Constants.he_costs[3],
        treat = treat,
        major_img = major_img,
        minor_img = minor_img
        )
        
    @staticmethod
    def js_vars(player):
        pass
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            player.activechoiceafterhe = False
        

        if player.he_page_form == 1:
            player.view_info = 1
            player.activechoiceafterhe = True
        elif player.he_page_form == 2:
            player.view_info = 2
            player.activechoiceafterhe = True
        elif player.he_page_form == -1:
            player.change_hi = True
            player.view_info = 0
            player.activechoiceafterhe = True
        elif player.he_page_form == 0:
            player.change_hi = False
            player.view_info = 0
            player.activechoiceafterhe = True
        
        import time
        participant.expiry = time.time() + Constants.timeout*60


class Payoff(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        if player.round_number == Constants.num_rounds:
            return True
        else: 
            return False
    @staticmethod
    def vars_for_template(player):
        player.calculate_payoff()
        return dict()


class WTP_1(Page):
    form_model = 'player'
    form_fields = ['wtp_g1']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        initial = 20
        return dict(
            initial=initial)


class WTP_2(Page):
    form_model = 'player'
    form_fields = ['wtp_g2']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_g1:
            general2 = 40
        else:
            general2 = 10

        return dict(
            general2=general2
        )


class WTP_3(Page):
    form_model = 'player'
    form_fields = ['wtp_g3']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_g1:
            if player.wtp_g2:
                general3 = 50
            else:
                general3 = 30
        else:
            if player.wtp_g2:
                general3 = 15
            else:
                general3 = 5

        return dict(
            general3=general3
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        wtp_order(player)


class WTP_4(Page):
    form_model = 'player'
    form_fields = ['wtp_p1']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        personal1 = 100
        return dict(
            personal1=personal1)


class WTP_5(Page):
    form_model = 'player'
    form_fields = ['wtp_p2']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_p1:
            personal2 = 200
        else:
            personal2 = 50

        return dict(
            personal2=personal2
        )


class WTP_6(Page):
    form_model = 'player'
    form_fields = ['wtp_p3']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_p1:
            if player.wtp_p2:
                personal3 = 250
            else:
                personal3 = 150
        else:
            if player.wtp_p2:
                personal3 = 75
            else:
                personal3 = 25

        return dict(
            personal3=personal3
        )


class WTP_7(Page):
    form_model = 'player'
    form_fields = ['wtp_p4']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        personal1 = 100
        return dict(
            personal1=personal1)


class WTP_8(Page):
    form_model = 'player'
    form_fields = ['wtp_p5']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_p4:
            personal2 = 200
        else:
            personal2 = 50

        return dict(
            personal2=personal2
        )


class WTP_9(Page):
    form_model = 'player'
    form_fields = ['wtp_p6']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        if player.wtp_p4:
            if player.wtp_p5:
                personal3 = 250
            else:
                personal3 = 150
        else:
            if player.wtp_p5:
                personal3 = 75
            else:
                personal3 = 25

        return dict(
            personal3=personal3
        )
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return upcoming_apps[0]

page_sequence = [Welcome, Instructions, Instructions_Review, Instructions_Status_Overview, Instructions_Health_Event, Instructions_Change_HI, Start, Personalized_information, Change_HI, Status_Overview, Health_event, Payoff, WTP_1, WTP_2, WTP_3, WTP_4, WTP_5, WTP_6, WTP_7, WTP_8, WTP_9]