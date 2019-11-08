from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy

import sched, time
import random
from random import randint
import uuid


cities=["New York", "Baltimore", "Charlotte", "Atlanta", "Orlando", "Austin", "Los Angeles", "Salt Lake City", "Chicago"]

s = sched.scheduler(time.time, time.sleep)
def write_weather(sc):
    cluster = Cluster(['c2.default.svc.cluster.local', 'c1.default.svc.cluster.local', 'c0.default.svc.cluster.local'],
        load_balancing_policy=RoundRobinPolicy(),
        port=9042)
    session = cluster.connect('starrynight')
    insert_id = randint(10000000, 99999999) # 8-digit uuid
    timestamp = uuid.uuid1()
    city = random.choice(cities)
    temperature = randint(10, 90)
    print("inserting: %s %s %s %s" % (insert_id, city, temperature, timestamp))
    session.execute(
        """
        INSERT INTO weather (id, location, temperature, timestamp)
        VALUES (%s, %s, %s, %s)
        """,
        (insert_id, city, temperature, timestamp)
    )
    s.enter(2, 1, write_weather, (sc,))

s.enter(2, 1, write_weather, (s,))
s.run()
