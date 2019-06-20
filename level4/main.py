import json
from functools import reduce
from itertools import groupby
import jsonpickle

from dateutil.parser import parse

from level4.worker import Worker

costs = {'interne': 126, 'medic': 270, 'interim': 480}
fixedInterimCommission = 80
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

    nbShift = len(shiftsForWorker)

    workerStatusPrice = costs[workerStatus]
    total = workerStatusPrice * (len(weekendShifts) * 2 + len(weekdayShifts))
    interim_ = workerStatus == 'interim'
    workersCost.append(Worker(k, total, nbShift, interim_))

workerCommission = (sum(c.price * 0.05 for c in workersCost))
interim_shifts = sum(map(lambda x: x.nbShift, filter(lambda d: d.isInterim, workersCost)))


with open('output.json', 'w', encoding='utf-8') as outfile:
    json.dump({"commission": {
        "pdg_fee": interim_shifts * fixedInterimCommission + workerCommission,
        "interim_shifts": interim_shifts
    }, 'workers': jsonpickle.encode(workersCost, unpicklable=False)}, outfile, ensure_ascii=False, indent=2)
