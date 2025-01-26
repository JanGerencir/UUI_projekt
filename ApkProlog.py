import re

class LogRezonator:
    def __init__(self):
        self.pravila = []  
        self.predikati = []  

    def dodaj_pravilo(self, pravilo):
        """Dodavanje pravila."""
        self.pravila.append(parsiraj_pravilo(pravilo))

    def dodaj_predikat(self, zaglavlje, tijelo):
        """Dodavanje predikata."""
        parsed_zaglavlje = parsiraj_pravilo(zaglavlje)
        parsed_tijelo = [parsiraj_pravilo(part.strip()) for part in tijelo]
        self.predikati.append((parsed_zaglavlje, parsed_tijelo))

    def unify(self, upit, pravilo):
        """Unifikacija upita i pravila."""
        if len(upit) != len(pravilo):
            return None

        substitution = {}
        for q, f in zip(upit, pravilo):
            if q == f:
                continue
            elif q.isupper():  
                substitution[q] = f
            elif f.isupper():
                substitution[f] = q
            else:
                return None  

        return substitution

    def resolve(self, upit, posjecen=None, depth=0, max_depth=10):
        """Rezolucija upita prema pravilima i predikatima."""
        if depth > max_depth:
            print(f"Prekoračena maksimalna dubina rekurzije za upit {upit}.")
            return []

        if posjecen is None:
            posjecen = set()

        upit_str = str(upit)
        if upit_str in posjecen:
            return []  
        posjecen.add(upit_str)

        rezultati = []
        for pravilo in self.pravila:
            substitution = self.unify(upit, pravilo)
            if substitution is not None:
                rezultati.append(substitution)

        for predikat in self.predikati:
            zaglavlje, tijelo = predikat
            substitution = self.unify(upit, zaglavlje)
            if substitution is not None:
                temp_rezultati = [substitution]
                for sub_upit in tijelo:
                    new_temp_rezultati = []
                    for temp in temp_rezultati:
                        resolved = self.resolve(self.primjeni_zamjenu(sub_upit, temp), posjecen, depth + 1, max_depth)
                        for r in resolved:
                            combined_result = temp.copy()
                            combined_result.update(r)
                            new_temp_rezultati.append(combined_result)
                    temp_rezultati = new_temp_rezultati
                rezultati.extend(temp_rezultati)

        return rezultati

    def primjeni_zamjenu(self, upit, substitution):
        """Primjena substitucije na upit."""
        return [substitution.get(q, q) for q in upit]

    def upit(self, prolog_upit):
        """Postavljanje upita."""
        upit = parsiraj_pravilo(prolog_upit)
        rezultati = self.resolve(upit)
        if rezultati:
            print(f"Upit {upit} je zadovoljen:")
            for result in rezultati:
                print(result)
        else:
            print(f"Upit {upit} nije zadovoljen.")

def parsiraj_pravilo(pravilo):
    """Parsira fakt u oblik liste."""
    pravilo = pravilo.strip()
    match = re.match(r"^(\w+)\(([^()]+)\)$", pravilo)
    if not match:
        raise ValueError(f"Pogrešan format: {pravilo}. Koristite npr. pravilo(X, Y)")
    predicate = match.group(1)
    arguments = [arg.strip() for arg in match.group(2).split(",")]
    return [predicate] + arguments

# CLI funkcionalnosti
def cli():
    print("Dobrodošli u aplikaciju za vježbanje Prologa!")
    lr = LogRezonator()

    while True:
        print("\nOpcije:")
        print("1. Dodaj pravilo")
        print("2. Dodaj predikat (Unesite glavu pa tijelo)")
        print("3. Postavi upit")
        print("4. Ispis pravila")
        print("5. Ispis predikata")
        print("6. Interaktivne vježbe")
        print("7. Izlaz")

        izbor = input("Odaberite opciju: ")

        if izbor == "1":
            prolog_pravilo = input("Unesite pravilo u Prolog sintaksi npr. roditelj(ivan, ivana): ")
            try:
                lr.dodaj_pravilo(prolog_pravilo)
                print(f"Pravilo {prolog_pravilo} dodan.")
            except ValueError as e:
                print(e)

        elif izbor == "2":
            zaglavlje = input("Unesite glavu predikata npr. predak(X, Y): ")
            tijelo = []
            print("Unesite tijelo predikata, jedno po jedno npr. roditelj(X, Z) Pritisnite Enter za kraj.")
            while True:
                part = input("Unesite dio tijela predikata: ")
                if not part:
                    break
                tijelo.append(part)
            try:
                lr.dodaj_predikat(zaglavlje, tijelo)
                print(f"Pravilo {zaglavlje} :- {', '.join(tijelo)} dodano.")
            except ValueError as e:
                print(e)

        elif izbor == "3":
            prolog_upit = input("Unesite upit u Prolog sintaksi npr. predak(ivan, ivana): ")
            try:
                lr.upit(prolog_upit)
            except ValueError as e:
                print(e)

        elif izbor == "4":
            print("Pravila:")
            for pravilo in lr.pravila:
                print(f"{pravilo[0]}({', '.join(pravilo[1:])}).")

        elif izbor == "5":
            print("Predikati:")
            for predikat in lr.predikati:
                zaglavlje = f"{predikat[0][0]}({', '.join(predikat[0][1:])})"
                tijelo = ", ".join([f"{b[0]}({', '.join(b[1:])})" for b in predikat[1]])
                print(f"{zaglavlje} :- {tijelo}.")

        elif izbor == "6":
            interaktivne_vjezbe(lr)

        elif izbor == "7":
            print("Doviđenja!")
            break

        else:
            print("Nevažeća opcija. Pokušajte ponovno.")

def interaktivne_vjezbe(lr):
    print("\nDobrodošli u interaktivne vježbe Prologa!")

    tocno = 0
    ukupno = 6

    print("Vježba 1: Napišite pravilo koji znači da Ivan voli Ivanu.")
    unos = input("Vaš unos: ")
    if unos.strip() == "voli(Ivan, Ivana)":
        print("Točno! Pravilo je dodano.")
        lr.dodaj_pravilo(unos)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: voli(Ivan, Ivana)")

    print("\nVježba 2: Napišite pravilo za predikat prijatelj(X, Y) koji znači da X voli Y i Y voli X.")
    zaglavlje = input("Unesite glavu pravila: ")
    tijelo = []
    print("Unesite tijelo pravila, jedno po jedno npr. voli(X, Y) Pritisnite Enter za kraj.")
    while True:
        dio = input("Dio tijela: ")
        if not dio:
            break
        tijelo.append(dio)

    if zaglavlje.strip() == "prijatelj(X, Y)" and tijelo == ["voli(X, Y)", "voli(Y, X)"]:
        print("Točno! Pravilo je dodano.")
        lr.dodaj_predikat(zaglavlje, tijelo)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: prijatelj(X, Y) :- voli(X, Y), voli(Y, X).")

    print("\nVježba 3: Napišite pravilo koji znači da Tina je sestra od Luke.")
    unos = input("Vaš unos: ")
    if unos.strip() == "sestra(Tina, Luka)":
        print("Točno! Pravilo je dodan.")
        lr.dodaj_pravilo(unos)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: sestra(Tina, Luka)")

    print("\nVježba 4: Napišite pravilo koji znači da Ana je prijatelj od Marka.")
    unos = input("Vaš unos: ")
    if unos.strip() == "prijatelj(Ana, Marko)":
        print("Točno! Pravilo je dodan.")
        lr.dodaj_pravilo(unos)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: prijatelj(Ana, Marko)")

    print("\nVježba 5: Napišite pravilo za predikat brat(X, Y) koji znači da su X i Y braća ako dijele iste roditelje.")
    zaglavlje = input("Unesite glavu pravila: ")
    tijelo = []
    print("Unesite tijelo pravila, jedno po jedno npr. roditelj(Z, X), roditelj(Z, Y) Pritisnite Enter za kraj.")
    while True:
        dio = input("Dio tijela: ")
        if not dio:
            break
        tijelo.append(dio)

    if zaglavlje.strip() == "brat(X, Y)" and tijelo == ["roditelj(Z, X)", "roditelj(Z, Y)"]:
        print("Točno! Pravilo je dodano.")
        lr.dodaj_predikat(zaglavlje, tijelo)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: brat(X, Y) :- roditelj(Z, X), roditelj(Z, Y)")

    print("\nVježba 6: Napišite pravilo za predikat unuk(X, Y) koji znači da je X unuk Y ako je roditelj Z roditelj X, a Y je roditelj Z.")
    zaglavlje = input("Unesite glavu pravila: ")
    tijelo = []
    print("Unesite tijelo pravila, jedno po jedno npr. roditelj(Z, X), roditelj(Y, Z). Pritisnite Enter za kraj.")
    while True:
        dio = input("Dio tijela: ")
        if not dio:
            break
        tijelo.append(dio)

    if zaglavlje.strip() == "unuk(X, Y)" and tijelo == ["roditelj(Z, X)", "roditelj(Y, Z)"]:
        print("Točno! Pravilo je dodano.")
        lr.dodaj_predikat(zaglavlje, tijelo)
        tocno += 1
    else:
        print("Netočno. Pravi unos je: unuk(X, Y) :- roditelj(Z, X), roditelj(Y, Z)")

    postotak = (tocno / ukupno) * 100
    print(f"\nTočnost: {postotak:.2f}%")

    if tocno == ukupno:
        print("Bravo! Sve ste točno riješili!")
    else:
        print("Dobar rezultat, ali može to i bolje! Pokušajte ponovno.")
        ponovi = input("Želite li ponoviti vježbe? (da/ne): ")
        if ponovi.lower() == "da":
            interaktivne_vjezbe(lr)

if __name__ == "__main__":
    cli()