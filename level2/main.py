import json
from itertools import groupby
import jsonpickle

from level1.worker import Worker

costs = {'interne': 126, 'medic': 270}
with open('data.json') as json_file:
    data = json.load(json_file)

shifts = data['shifts']
workers = data['workers']

shifts = sorted(shifts, key=lambda x: x['user_id'])

workersCost = []

for k, g in groupby(shifts, key=lambda x: x['user_id']):
    worker = filter(lambda d: d['id'] == k, workers)

    workerStatus = (list(worker)[0]['status'])
    workerStatusPrice = costs[workerStatus]

    total = workerStatusPrice * (len(list(g)))
    workersCost.append(Worker(k, total))
print(workersCost)
with open('output.json', 'w', encoding='utf-8') as outfile:
    json.dump({'workers': jsonpickle.encode(workersCost, unpicklable=False)}, outfile, ensure_ascii=False, indent=2)
