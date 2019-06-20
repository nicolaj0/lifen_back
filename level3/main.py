import json
from itertools import groupby
import jsonpickle

from level1.worker import Worker
from dateutil.parser import parse

costs = {'interne': 126, 'medic': 270}

with open('data.json') as json_file:
    data = json.load(json_file)

shifts = data['shifts']
workers = data['workers']

shifts = filter(lambda x: x['user_id'] is not None, shifts)
shifts = sorted(shifts, key=lambda x: x['user_id'])

workersCost = []

for k, g in groupby(shifts, key=lambda x: x['user_id']):
    worker = list(filter(lambda d: d['id'] == k, workers))
    shiftsForWorker = list(g)
    workerStatus = (worker[0]['status'])
    shiftCostMultiplier = list(map(lambda x: x['start_date'], shiftsForWorker))
    weekendShifts = list(filter(lambda d: parse(d).weekday() in (5, 6), shiftCostMultiplier))
    weekdayShifts = list(filter(lambda d: parse(d).weekday() not in (5, 6), shiftCostMultiplier))

    workerStatusPrice = costs[workerStatus]
    total = workerStatusPrice * (len(weekendShifts)*2 + len(weekdayShifts))
    workersCost.append(Worker(k, total))
print(workersCost)

with open('output.json', 'w', encoding='utf-8') as outfile:
    json.dump({'workers': jsonpickle.encode(workersCost, unpicklable=False)}, outfile, ensure_ascii=False, indent=2)
