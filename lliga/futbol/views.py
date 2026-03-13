from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Lliga


def standings(request, lliga_id=None):
	"""Compute a standings table for a league and render it.

	The heavy lifting (points, wins, draws, goals) is done here in the view
	so the template only renders the prepared data.
	"""
	if lliga_id:
		lliga = get_object_or_404(Lliga, pk=lliga_id)
	else:
		lliga = Lliga.objects.first()
		if not lliga:
			return render(request, 'futbol/standings.html', {'lliga': None, 'table': []})

	equips = lliga.equips.all()

	# initialize stats
	stats = {}
	for e in equips:
		stats[e.id] = {
			'equip': e,
			'points': 0,
			'played': 0,
			'wins': 0,
			'draws': 0,
			'losses': 0,
			'gf': 0,
			'ga': 0,
		}

	# aggregate over matches
	for partit in lliga.partits.all():
		gl = partit.gols_local()
		gv = partit.gols_visitant()
		local = partit.equip_local
		visitant = partit.equip_visitant

		if local.id not in stats or visitant.id not in stats:
			continue

		stats[local.id]['played'] += 1
		stats[visitant.id]['played'] += 1
		stats[local.id]['gf'] += gl
		stats[local.id]['ga'] += gv
		stats[visitant.id]['gf'] += gv
		stats[visitant.id]['ga'] += gl

		if gl > gv:
			stats[local.id]['wins'] += 1
			stats[local.id]['points'] += 3
			stats[visitant.id]['losses'] += 1
		elif gl < gv:
			stats[visitant.id]['wins'] += 1
			stats[visitant.id]['points'] += 3
			stats[local.id]['losses'] += 1
		else:
			stats[local.id]['draws'] += 1
			stats[visitant.id]['draws'] += 1
			stats[local.id]['points'] += 1
			stats[visitant.id]['points'] += 1
            
	table = []
	for s in stats.values():
		s['gd'] = s['gf'] - s['ga']
		table.append(s)

	# sort by points, goal difference, goals for, name
	table.sort(key=lambda x: (-x['points'], -x['gd'], -x['gf'], x['equip'].nom))

	return render(request, 'futbol/standings.html', {'lliga': lliga, 'table': table})
