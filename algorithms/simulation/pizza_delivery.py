import simpy
import random

RESTAURANT_DELAY = 2
CUSTOMER_DELAY = 2
OVEN_CAPACITY = 4
DRIVER_SPEED = 30
COOK_TIME = 10
FRESH_PIZZA_TEMP = 150 #F Degrees
COOL_RATE = 1 #PER MIN
order_temp_list = []


class PizzaRestaurant:

    def __init__(self, env, delivery_radius, num_drivers, order_rate):
        self.delivery_radius = delivery_radius
        self.order_rate = order_rate
        self.env = env
        self.driver = simpy.Resource(env, num_drivers)
        self.oven_slot = simpy.Resource(env, OVEN_CAPACITY)

    def cook_order(self, customer):
        yield self.env.timeout(COOK_TIME)

    def deliver_order(self, customer):
        customer_dist = self.delivery_radius * (random.uniform(0.1, 1) ** 0.5)
        print("Order distance :", customer_dist)
        delivery_time = customer_dist/30 #time in hours
        print("Total Delivery time:", delivery_time*60)
        pizza_temp = 150-(delivery_time*60)*1
        if pizza_temp > 0:
            order_temp_list.append(pizza_temp)
        else:
            order_temp_list.append(0)
        yield self.env.timeout(delivery_time*60)
        yield self.env.timeout(2)  # customer delay


def process_order(env, customer, pizzaden):

    with pizzaden.oven_slot.request() as request:
        yield request
        yield env.process(pizzaden.cook_order(customer))

    with pizzaden.driver.request() as request:
        yield request
        yield env.timeout(2) #depart delay
        yield env.process(pizzaden.deliver_order(customer))


def run_restaurant(env, delivery_radius, num_drivers, order_rate):
    pizza_den = PizzaRestaurant(env, delivery_radius, num_drivers, order_rate)
    customer = 0
    while True:
        customer += 1
        yield env.timeout(order_rate)
        print("Order Placed:", env.now)
        env.process(process_order(env, customer, pizza_den))


def main():
    # Setup
    # random.seed(42)
    env = simpy.Environment()
    env.process(run_restaurant(env, 10, 5, 5))
    env.run(until=180)
    print(order_temp_list)


if __name__ == "__main__":
    main()
