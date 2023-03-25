from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

#need to solve: the state should be the same for the sender and receiver with the same group id.
#true_state = 1 means the color of the ball is RED, while true_type = 1 means the sender is COMMITTED.
#For each pair of sender and receiver, there is one true state of nature and one true type.
#For the receiver, we define the current belief as the initial prior.
#In the first stage, sender chooses the communication plan. We impose that the sender only senders message 1 when state is 1.
#The sender only needs to decide x1 which is the probability of sending message Red when the state is Blue.
class init_calc(WaitPage):
    def after_all_players_arrive(self):
        self.group.get_state()
        self.group.get_type()

class Sender_instruction(Page):
    def is_displayed(self):
        return (self.player.id_in_group == 1) and (self.round_number == 1)

class Receiver_instruction(Page):
    def is_displayed(self):
        return (self.player.id_in_group == 2) and (self.round_number == 1)
#
#
# class cost_report(Page):
#     form_model = 'player'
#     form_fields = ['cost_report']
#
#     def is_displayed(self):
#         return self.round_number == 1
#
#
# class cost_result(Page):
#     def is_displayed(self):
#         return self.round_number == 1

class Sender_decision(Page):
    form_model = 'group'
    form_fields = ['x','y']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        prior = round(Constants.initial_prior*100)
        initial_x = random.randint(1,99)
        minus_x= round(100 - initial_x)
        initial_y = random.randint(1,99)
        minus_y = round(100 - initial_y)
        return{'prior':prior,
               'onemp':100 - prior,
               'initial_x': initial_x,
               'minus_x': minus_x,
               'initial_y': initial_y,
               'minus_y': minus_y
               }

"""
class Sender_commit(Page):
    form_model = 'group'
    form_fields = ['x']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        prior = round(Constants.initial_prior*100)
        initial_x = random.randint(1,99)
        minus_x= round(100 - initial_x)
        return{'prior':prior,
               'onemp':100 - prior,
               'initial_x': initial_x,
               'minus_x': minus_x,
               }

#The sender observes the true stage first, and then chooses the revision plan.
#Edit the true state presentation in templates.

class Sender_revise(Page):
    form_model = 'group'
    form_fields = ['y']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        prior = round(Constants.initial_prior*100)
        initial_y = random.randint(1,99)
        minus_y = round(100 - initial_y)
        return{'prior':prior,
               'onemp': 100 - prior,
               'initial_y': initial_y,
               'minus_y': minus_y,
               }
"""



class WaitforP1(WaitPage):
    def after_all_players_arrive(self):
        self.group.posterior_rx = round(Constants.initial_prior/(Constants.initial_prior + (1 - Constants.initial_prior)*(1 - self.group.x)),2)
        self.group.posterior_ry = round(Constants.initial_prior/(Constants.initial_prior + (1 - Constants.initial_prior)*(1 - self.group.y)),2)
        if self.group.true_state == 1:
            self.group.message = 1
        elif self.group.true_type == 1:
            self.group.message = random.choices([0,1], weights = [self.group.x, 1 - self.group.x])[0]
        else:
            self.group.message = random.choices([0,1], weights = [self.group.y, 1- self.group.y])[0]


#The receiver will also be shown the probability rho
class Receiver_observe(Page):
    form_model = 'group'
    form_fields = ['decision']

    def is_displayed(self):
       return self.player.id_in_group == 2

    def decision_choices(self):
        return [
                [1, 'Observe ($0.5)'],
                [0, 'Not observe ($0)'],
            ]

    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        init_prior = round(Constants.initial_prior*100)
        posterior_r = self.group.posterior_rx
        posterior_b = 1
        omip = round(100 - init_prior)
        return{'display_x':display_x,
               'display_xm':display_xm,
               'init_prior':init_prior,
               'omip': omip,
               'posterior_r': posterior_r,
               'posterior_b':posterior_b}

#Displayed only to the receiver who does not observe.
class Receiver_guess_no(Page):
    form_model = 'group'
    form_fields = ['red_guess']

    def is_displayed(self):
        return (self.player.id_in_group == 2) and (self.group.decision == 0)

    def red_guess_choices(self):
        return [
                [1, 'Red'],
                [0, 'Blue'],
            ]


    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        display_y = round(self.group.y*100)
        display_ym = 100 - display_y
        init_prior = round(Constants.initial_prior*100)
        posterior_r = self.group.posterior_rx
        posterior_b = 1
        omip = round(100 - init_prior)
        return{'display_x':display_x,
               'display_xm':display_xm,
               'display_y':display_y,
               'display_ym':display_ym,
               'init_prior':init_prior,
               'omip': omip,
               'posterior_r':posterior_r,
               'posterior_b':posterior_b}


#Displayed only to the receiver who observes but the result is still plan 1.
class Receiver_guess_o1(Page):
    form_model = 'group'
    form_fields = ['red_guess']

    def is_displayed(self):
        return (self.player.id_in_group == 2) and (self.group.decision == 1) and (self.group.true_type == 1)

    def red_guess_choices(self):
        return [
                [1, 'Red'],
                [0, 'Blue'],
            ]


    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        display_y = round(self.group.y*100)
        display_ym = 100 - display_y
        init_prior = round(Constants.initial_prior*100)
        omip = round(100 - init_prior)
        return{'display_x':display_x,
               'display_xm':display_xm,
               'display_y':display_y,
               'display_ym':display_ym,
               'init_prior':init_prior,
               'omip': omip}


class Receiver_guess_o2(Page):
    form_model = 'group'
    form_fields = ['red_guess']

    def is_displayed(self):
        return (self.player.id_in_group == 2) and (self.group.decision == 1) and (self.group.true_type == 0)

    def red_guess_choices(self):
        return [
                [1, 'Red'],
                [0, 'Blue'],
            ]


    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        display_y = round(self.group.y*100)
        display_ym = 100 - display_y
        init_prior = round(Constants.initial_prior*100)
        omip = round(100 - init_prior)
        return{'display_x':display_x,
               'display_xm':display_xm,
               'display_y':display_y,
               'display_ym':display_ym,
               'init_prior':init_prior,
               'omip': omip}


class Waitforall(WaitPage):

    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        if self.group.message == 1:
            if self.group.red_guess == self.group.true_state:
                p2.round_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
                p1.other_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
            else:
                p2.round_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost
                p1.other_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost
            if self.group.red_guess == 1:
                p1.round_payoff = Constants.sender_payoffs[1]
                p2.other_payoff = Constants.sender_payoffs[1]
            else:
                p1.round_payoff = Constants.sender_payoffs[0]
                p2.other_payoff = Constants.sender_payoffs[0]
        else:
            p1.round_payoff = Constants.sender_payoffs[0]
            p2.other_payoff = Constants.sender_payoffs[0]
            if self.group.true_state == 0:
                p2.round_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
                p1.other_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
            else:
                p2.round_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost
                p1.other_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost

        if self.group.message == 1:
            self.group.guess = self.group.red_guess
        else:
            self.group.guess = 0

        for p in self.group.get_players():
            app1_list = p.participant.vars.get('app1_payoffs',[])
            app1_list.append(p.round_payoff)
            p.participant.vars['app1_payoffs'] = app1_list

        for p in self.group.get_players():
            if self.round_number == Constants.num_rounds:
                payoff_list = p.participant.vars.get('payoffs', [])
                app1_list = p.participant.vars.get('app1_payoffs', [])
                payoff_list.append(app1_list)
                p.participant.vars['payoffs'] = payoff_list

"""
class Waitforall(WaitPage):

    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        if self.group.message == 1:
            if self.group.red_guess == self.group.true_state:
                p2.round_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
            else:
                p2.round_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost
            if self.group.red_guess == 1:
                p1.round_payoff = Constants.sender_payoffs[1]
            else:
                p1.round_payoff = Constants.sender_payoffs[0]
        else:
            if self.group.blue_guess == self.group.true_state:
                p2.round_payoff = Constants.receiver_payoffs[1] - self.group.decision*Constants.observation_cost
            else:
                p2.round_payoff = Constants.receiver_payoffs[0] - self.group.decision*Constants.observation_cost
            if self.group.blue_guess == 1:
                p1.round_payoff = Constants.sender_payoffs[1]
            else:
                p1.round_payoff = Constants.sender_payoffs[0]

        for p in self.group.get_players():
            app1_list = p.participant.vars.get('app1_payoffs',[])
            app1_list.append(p.round_payoff)
            p.participant.vars['app1_payoffs'] = app1_list
"""


class Results_C1(Page):

    def is_displayed(self):
        return (self.group.true_type == 1)

    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        display_y = round(self.group.y*100)
        display_ym = 100 - display_y
        posterior_rx = round(self.group.posterior_rx*100)
        posterior_ry = round(self.group.posterior_ry*100)
        posterior_bx = 100 - posterior_rx
        posterior_by = 100 - posterior_ry
        return{'display_x': display_x,
               'display_xm': display_xm,
               'display_y': display_y,
               'display_ym': display_ym,
               'posterior_rx': posterior_rx,
               'posterior_ry': posterior_ry,
               'posterior_bx': posterior_bx,
               'posterior_by': posterior_by
               }


class Results_C2(Page):

    def is_displayed(self):
        return (self.group.true_type == 0)

    def vars_for_template(self):
        display_x = round(self.group.x*100)
        display_xm = 100 - display_x
        display_y = round(self.group.y*100)
        display_ym = 100 - display_y
        posterior_rx = round(self.group.posterior_rx*100)
        posterior_ry = round(self.group.posterior_ry*100)
        posterior_bx = 100 - posterior_rx
        posterior_by = 100 - posterior_ry
        return{'display_x': display_x,
               'display_xm': display_xm,
               'display_y': display_y,
               'display_ym': display_ym,
               'posterior_rx': posterior_rx,
               'posterior_ry': posterior_ry,
               'posterior_bx': posterior_bx,
               'posterior_by': posterior_by
               }

page_sequence = [init_calc, Sender_instruction, Receiver_instruction, Sender_decision, WaitforP1, Receiver_observe, Receiver_guess_no, Receiver_guess_o1,Receiver_guess_o2,Waitforall, Results_C1, Results_C2]
