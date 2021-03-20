import simpy
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('WebAgg')
# matplotlib.use('Agg')
customer_data = {}


RESTAURANT_DELAY = 2
CUSTOMER_DELAY = 2
OVEN_CAPACITY = 4
DRIVER_SPEED = 30
COOK_TIME = 10
FRESH_PIZZA_TEMP = 150 #F Degrees
COOL_RATE = 1 #PER MIN
order_temp_list = []
last_completed_order=0
oven_util = []
driver_util = []


class PizzaRestaurant:

    def __init__(self, env, delivery_radius, num_drivers, order_rate):
        self.delivery_radius = delivery_radius
        self.order_rate = order_rate
        self.env = env
        self.driver = simpy.Resource(env, num_drivers)
        self.oven_slot = simpy.Resource(env, OVEN_CAPACITY)

    def cook_order(self, customer):
        print(f"Pizza going to oven for {customer} at {self.env.now}")
        customer_data[customer]["going to oven"] = self.env.now
        yield self.env.timeout(COOK_TIME)
        print(f"Pizza ready for {customer} at {self.env.now}")
        customer_data[customer]["order ready"] = self.env.now

    def deliver_order(self, customer):
        customer_dist = self.delivery_radius * (random.uniform(0.1, 1) ** 0.5)
        print(f"Order distance for {customer}:", customer_dist)
        customer_data[customer]["order distance"] = customer_dist
        delivery_time = customer_dist/30 #time in hours
        print(f"Total Delivery time for {customer}", delivery_time*60)
        customer_data[customer]["estimated time to deliver"] = delivery_time*60
        pizza_temp = 150-(delivery_time*60)*1
        if pizza_temp > 0:
            order_temp_list.append(pizza_temp)
            customer_data[customer]["pizza temp"] = pizza_temp
        else:
            order_temp_list.append(0)
            customer_data[customer]["pizza temp"] = 0
        yield self.env.timeout(delivery_time*60)
        yield self.env.timeout(2)  # customer delay
        print(f"order delivered for {customer}", self.env.now)
        customer_data[customer]["order delivered"] = self.env.now
        global last_completed_order
        last_completed_order = customer
        yield self.env.timeout(delivery_time * 60)


def process_order(env, customer, pizzaden):

    with pizzaden.oven_slot.request() as request:
        yield request
        yield env.process(pizzaden.cook_order(customer))

    with pizzaden.driver.request() as request:
        yield request
        yield env.timeout(2) #depart delay
        print(f"Pizza out for delivery for {customer} at {env.now}")
        customer_data[customer]["out for delivery"] = env.now
        yield env.process(pizzaden.deliver_order(customer))


def run_restaurant(env, delivery_radius, num_drivers, order_rate):
    pizza_den = PizzaRestaurant(env, delivery_radius, num_drivers, order_rate)
    customer = 0
    while True:
        customer += 1
        yield env.timeout(order_rate)
        customer_data[customer] = {}
        print("Order Placed:", env.now)
        customer_data[customer]["order placed"] = env.now
        env.process(process_order(env, customer, pizza_den))
        print("Occupied drivers ", pizza_den.driver.count)
        driver_util.append(pizza_den.driver.count)
        print("Occupied slots in oven ", pizza_den.oven_slot.count)
        oven_util.append(pizza_den.oven_slot.count)


def plot_data(data, y="weights", x="values"):
    import matplotlib.pyplot as plt
    plt.hist(data)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.savefig(f"{x}_{y}.png")
    plt.close()


def main():
    # Setup
    random.seed(42)
    env = simpy.Environment()
    env.process(run_restaurant(env, 10, 5, 5))
    env.run(until=180)
    print(customer_data)
    cp_one = []
    cp_two=[]
    cp_three=[]
    for i in list(customer_data.values())[:last_completed_order]:
        cp_one.append(i["going to oven"] - i["order placed"])
        cp_two.append(i['out for delivery'] - i["order ready"])
        cp_three.append(i['order delivered'] - i['order placed'])
    plot_data(cp_one, x="delay going to oven")
    plot_data(cp_two, x="delay to pick up order")
    plot_data(cp_three, x="total time")
    print("Average oven utilisation", sum(oven_util) / len(oven_util))
    print("Average driver utilisation", sum(driver_util) / len(driver_util))


if __name__ == "__main__":
    main()
