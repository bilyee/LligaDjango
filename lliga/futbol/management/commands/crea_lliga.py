from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
from datetime import time
 
from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga, temporada="temporada" )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(ciutat=ciutat,nom=nom,lliga=lliga)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                edat = 25
                jugador = Jugador(nom=nom,posicio=posicio,
                    edat=edat,equip=equip)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(equip_local=local,equip_visitant=visitant,lliga=lliga)
                    partit.equip_local = local
                    partit.equip_visitant = visitant
                    partit.lliga = lliga
                    mes = randint(1, 12)
                    dia = randint(1, 28)
                    partit.data = timezone.now() + timedelta(days=mes*30+dia)
                    partit.save()

                    # Goles
                    for _ in range(randint(0, 7)):
                        hora = randint(0, 23)
                        minut = randint(0, 59)
                        segon = randint(0, 59)

                        equip_gol = local if randint(0, 1) == 0 else visitant
                        jugador = equip_gol.jugadors.order_by('?').first()

                        Event.objects.create(
                            partit=partit,
                            tipus=Event.EventType.GOL,
                            temps=time(hour=hora, minute=minut, second=segon),
                            equip=equip_gol,
                            jugador=jugador
                        )