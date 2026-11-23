"""Regras do cronograma e objetivo, separadas para revisao conjunta."""


def adicionar_inicio_unico(modelo, variaveis):
    import pulp

    for a, dias in variaveis.inicios.items():
        modelo += pulp.lpSum(variaveis.x[a][t] for t in dias) == 1, f"inicio_unico_{a}"


def adicionar_precedencias(modelo, variaveis, precedencias):
    S, F = variaveis.S, variaveis.F
    for k, p in enumerate(precedencias):
        i, j = p["predecessora"], p["sucessora"]
        lag = int(p.get("lag_dias", 0) or 0)
        tipo = p.get("tipo_vinculo", "TI") or "TI"
        if tipo == "TI":
            regra = S[j] >= F[i] + lag
        elif tipo == "II":
            regra = S[j] >= S[i] + lag
        elif tipo == "TT":
            regra = F[j] >= F[i] + lag
        elif tipo == "IT":
            regra = F[j] >= S[i] + lag
        else:
            raise ValueError(f"Tipo de vinculo invalido em {i}->{j}: {tipo}.")
        modelo += regra, f"prec_{k}"


def adicionar_capacidade(modelo, variaveis, duracoes, papeis, capacidades):
    import pulp

    for equipe in sorted({p for lista in papeis.values() for p in lista}):
        # Eventos de duracao zero permanecem na rede, sem ocupacao de equipe.
        usa = [a for a in duracoes if duracoes[a] > 0 and equipe in papeis[a]]
        for t in range(variaveis.horizonte):
            ocupacao = pulp.lpSum(
                variaveis.x[a][tau]
                for a in usa
                for tau in range(max(0, t - duracoes[a] + 1), t + 1)
                if tau in variaveis.x[a]
            )
            modelo += ocupacao <= capacidades[equipe], f"cap_{equipe}_{t}"


def definir_prazo_e_objetivo(modelo, variaveis):
    modelo += variaveis.Cmax
    for a in variaveis.F:
        # O dia zero e o primeiro dia, inclusive para o ultimo evento d=0.
        modelo += variaveis.Cmax >= variaveis.F[a] + 1, f"mksp_{a}"


def adicionar_restricoes(modelo, variaveis, precedencias, duracoes, papeis, capacidades):
    adicionar_inicio_unico(modelo, variaveis)
    adicionar_precedencias(modelo, variaveis, precedencias)
    adicionar_capacidade(modelo, variaveis, duracoes, papeis, capacidades)
    definir_prazo_e_objetivo(modelo, variaveis)
