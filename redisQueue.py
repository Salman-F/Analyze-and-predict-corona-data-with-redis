import redis

# Creating Connection to Redis Server on Raspberry Pi
r = redis.Redis(host='192.168.137.234', port='6379', password='redis', decode_responses=True)

r.set('cat', 'garfield')
val = r.get('cat')
print(val)
r.set('car', 'daimler')
print(r.get('car'))
