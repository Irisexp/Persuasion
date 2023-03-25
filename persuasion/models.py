from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random

author = 'Junya Zhou'

doc = """
Your app description
"""

#true_state represents whether the state is 1 (good) or 0(bad), true_type represents whether the sender is committed or not(1 committed, 0 uncommitted).

class Constants(BaseConstants):
    name_in_url = 'persuasion'
    players_per_group = 2
    num_rounds = 3

    initial_prior = 1/3
    receiver_payoffs = [c(0), c(12)]
    sender_payoffs = [c(0), c(12)]
    rho = 0.7
    minusrho = 0.3
    observation_cost = c(1)

class Subsession(BaseSubsession):

    def creating_session(self):
        self.group_randomly(fixed_id_in_group = True)

class Group(BaseGroup):

#state variable
    true_type = models.IntegerField()

    true_state = models.IntegerField()

#sender variable
    x = models.FloatField(max = 1, min= 0, initial=0.0)

    y = models.FloatField(max = 1, min= 0, initial=0.0)

    message = models.IntegerField()

#receiver variable
    observation = models.IntegerField()

    red_guess = models.IntegerField()

    blue_guess = models.IntegerField()

    posterior_rx = models.FloatField()

    posterior_ry = models.FloatField()

    def get_state(self):
        self.true_state = random.choices([0,1], weights = [1 - Constants.initial_prior, Constants.initial_prior])[0]
        return self.true_state

    def get_type(self):
        self.true_type = random.choices([0,1], weights = [1 - Constants.rho, Constants.rho])[0]
        return self.true_type

class Player(BasePlayer):

    round_payoff = models.CurrencyField()

    def role(self):
        if self.id_in_group == 1:
            return 'Sender'
        else:
            return 'Receiver'
