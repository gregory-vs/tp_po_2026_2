"""Gera os graficos de resultados para os slides (PNG em slides-finais/figuras/).

Le a rodada de sensibilidade mais recente em resultados/ (gerada por
codigo/sensibilidade.py). Nao roda modelo nem CBC.

Requer matplotlib, que nao e necessario para o modelo:
    .\\.venv\\Scripts\\python.exe -m pip install matplotlib
Uso, na raiz do repo:
    .\\.venv\\Scripts\\python.exe codigo\\graficos_slides.py
"""
from __future__ import annotations

import glob
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "slides-finais", "figuras")

# cores (paleta categorica validada; texto sempre em tinta neutra)
AZUL = "#2a78d6"      # emissao / otimo comprovado
LARANJA = "#eb6834"   # analise do cliente
CINZA = "#a3a29d"     # contexto (referencia, equipes)
CINZA_CLARO = "#dedcd5"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRADE = "#e6e4dd"

plt.rcParams.update({
    "font.size": 15, "axes.edgecolor": TINTA_2, "axes.labelcolor": TINTA_2,
    "xtick.color": TINTA_2, "ytick.color": TINTA, "text.color": TINTA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 100, "savefig.dpi": 220, "savefig.bbox": "tight",
})


def ultima_rodada():
    arqs = sorted(glob.glob(os.path.join(RAIZ, "resultados", "sensibilidade-*.json")))
    with open(arqs[-1], encoding="utf-8") as f:
        return json.load(f), os.path.basename(arqs[-1])


def cenario(lista, nome):
    for c in lista:
        if c["cenario"] == nome:
            return c
    raise KeyError(nome)


def salvar(fig, nome):
    os.makedirs(SAIDA, exist_ok=True)
    fig.savefig(os.path.join(SAIDA, nome), facecolor="white")
    plt.close(fig)
    print("gravado:", os.path.join("slides-finais", "figuras", nome))


def barras(ax, rotulos, valores, cores, fmt="{:d}", deslocamento=3):
    y = range(len(rotulos))
    ax.barh(y, valores, color=cores, height=0.62, edgecolor="white", linewidth=2)
    ax.set_yticks(list(y), rotulos)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, color=GRADE, linewidth=1)
    ax.set_axisbelow(True)
    for i, v in enumerate(valores):
        ax.text(v + deslocamento, i, fmt.format(v), va="center", color=TINTA,
                fontsize=15, fontweight="bold")


def g1_prazos(d, cbc_prazo=307):
    """Prazo total: referencia, CBC e os dois otimos."""
    rot = ["Cronograma praticado", "CBC (parou por tempo)",
           "Ótimo com liberações\n(realista)", "Ótimo, tudo liberado\nno início (limite)"]
    val = [d["referencia_dias"], cbc_prazo, d["base_com_liberacoes"]["prazo"],
           d["heuristica_prazo"]]
    cores = [CINZA, CINZA, AZUL, AZUL]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    barras(ax, rot, val, cores)
    ref = d["referencia_dias"]
    for i in (2, 3):
        ganho = ref - val[i]
        ax.text(val[i] + 48, i, f"−{ganho} dias ({100 * ganho / ref:.1f}%)".replace(".", ","),
                va="center", color=TINTA_2, fontsize=14)
    ax.set_xlim(0, 400)
    ax.set_xlabel("prazo total (dias úteis)")
    ax.text(0, -0.85, "Azul: ótimo comprovado (cronograma viável = limite inferior)",
            fontsize=12, color=TINTA_2, transform=ax.get_yaxis_transform())
    salvar(fig, "01-prazos.png")


def g2_sensibilidade(d):
    """Efeito de cada mudanca na base com liberacoes (285)."""
    lib = d["base_com_liberacoes"]["cenarios"]
    itens = [
        ("Todas as equipes +1", "todas as equipes +1", CINZA),
        ("Todas as equipes −1", "todas as equipes -1 (minimo 1)", CINZA),
        ("Análise do cliente em até 5 dias", "analise do cliente em ate 5 dias", LARANJA),
        ("Análise do cliente 50% mais rápida", "analise 50% mais rapida", LARANJA),
        ("Caixilhos 20% mais rápido", "disciplina CXO 20% mais rapida", AZUL),
        ("Zonas do AP de ARQ em paralelo", "torres do AP final de arquitetura em paralelo", AZUL),
        ("Arquitetura 20% mais rápida", "disciplina ARQ 20% mais rapida", AZUL),
        ("Emissão 10% mais rápida", "emissao 10% mais rapida", AZUL),
        ("Emissão 20% mais rápida", "emissao 20% mais rapida", AZUL),
    ]
    rot = [r for r, _, _ in itens]
    val = [-cenario(lib, n)["variacao_dias"] for _, n, _ in itens]
    cores = [c for _, _, c in itens]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    barras(ax, rot, val, cores, deslocamento=0.4)
    ax.set_xlim(0, 25)
    ax.set_xlabel(f"dias a menos no prazo (base de {d['base_com_liberacoes']['prazo']} dias)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=CINZA, label="equipes"),
                       Patch(color=LARANJA, label="análise do cliente"),
                       Patch(color=AZUL, label="emissão do projetista")],
              loc="upper right", frameon=False, fontsize=13)
    salvar(fig, "02-sensibilidade-285.png")


def g3_curva(d):
    """Reducao de emissao x reducao de analise (base com liberacoes)."""
    lib = d["base_com_liberacoes"]["cenarios"]
    pct = [0, 10, 20, 30, 50]
    emi = [0] + [cenario(lib, f"emissao {p}% mais rapida")["variacao_dias"] for p in pct[1:]]
    anl = [0] + [cenario(lib, f"analise {p}% mais rapida")["variacao_dias"] for p in pct[1:]]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(pct, emi, color=AZUL, linewidth=2.5, marker="o", markersize=9,
            markeredgecolor="white", markeredgewidth=2)
    ax.plot(pct, anl, color=LARANJA, linewidth=2.5, marker="s", markersize=9,
            markeredgecolor="white", markeredgewidth=2)
    ax.text(51, emi[-1], f"emissão do projetista (−{-emi[-1]})", va="center", fontsize=14)
    ax.text(51, anl[-1], f"análise do cliente (−{-anl[-1]})", va="center", fontsize=14)
    ax.text(10, emi[1] - 3.2, f"−{-emi[1]}", ha="center", fontsize=14, fontweight="bold")
    ax.set_xticks(pct, [f"{p}%" for p in pct])
    ax.set_xlim(0, 50)
    ax.set_ylim(-40, 3)
    ax.yaxis.grid(True, color=GRADE, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xlabel("redução da duração")
    ax.set_ylabel("variação do prazo (dias)")
    salvar(fig, "03-emissao-x-analise.png")


ROTULO_TIPO = {"EMISSAO": "Emissão", "ANALISE": "Análise"}
ROTULO_DISC = {"ARQ": "arquitetura", "CXO": "caixilhos"}


def g4_gantt(d):
    """Cadeia que define os 285 dias."""
    cad = d["base_com_liberacoes"]["cadeia_que_define_o_prazo"]
    prazo = d["base_com_liberacoes"]["prazo"]
    linhas = [("Espera pelo estudo preliminar\n(fora da base)", 0, cad[0]["inicio_mais_cedo"], CINZA_CLARO)]
    zona = 0
    for c in cad:
        rot = f"{ROTULO_TIPO[c['tipo']]} {ROTULO_DISC.get(c['disciplina'], c['disciplina'])} {c['fase']}"
        if c["id"] in ("T141",):
            rot = "Mapas de esquadrias (ARQ)"
        elif c["tipo"] == "EMISSAO" and c["disciplina"] == "ARQ" and c["fase"] == "AP":
            zona += 1
            rot = f"Emissão ARQ AP, zona {zona}"
        elif c["tipo"] == "ANALISE":
            rot = "Análise do cliente"
        cor = AZUL if c["tipo"] == "EMISSAO" else LARANJA
        linhas.append((rot, c["inicio_mais_cedo"], c["duracao"], cor))
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for i, (rot, ini, dur, cor) in enumerate(linhas):
        ax.barh(i, dur, left=ini, color=cor, height=0.64, edgecolor="white", linewidth=1.5)
    ax.set_yticks(range(len(linhas)), [r for r, *_ in linhas], fontsize=12)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, prazo + 5)
    ax.set_xticks([0, 50, 100, 150, 200, 250, prazo])
    ax.xaxis.grid(True, color=GRADE, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xlabel("dia")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=AZUL, label="emissão do projetista"),
                       Patch(color=LARANJA, label="análise do cliente")],
              loc="lower left", frameon=False, fontsize=12)
    salvar(fig, "04-cadeia-285.png")


def g5_equipes(d):
    """Equipes nas duas versoes da base: +1 e -1 em todas."""
    livre = {c["cenario"]: c for c in d["cenarios"] if c["grupo"] == "equipes"}
    lib = d["base_com_liberacoes"]["cenarios"]
    base_l, base_r = d["heuristica_prazo"], d["base_com_liberacoes"]["prazo"]
    grupos = ["equipes −1", "capacidade atual", "equipes +1"]
    v_livre = [livre["todas as equipes -1 (minimo 1)"]["melhor_viavel"], base_l,
               livre["todas as equipes +1"]["melhor_viavel"]]
    v_lib = [cenario(lib, "todas as equipes -1 (minimo 1)")["melhor_viavel"], base_r,
             cenario(lib, "todas as equipes +1")["melhor_viavel"]]
    fig, ax = plt.subplots(figsize=(8, 4.0))
    x = range(3)
    w = 0.36
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], v_lib, w, color=AZUL, label="com liberações")
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], v_livre, w, color=CINZA, label="tudo liberado no início")
    prova_livre = [livre["todas as equipes -1 (minimo 1)"]["otimo_comprovado"], True,
                   livre["todas as equipes +1"]["otimo_comprovado"]]
    prova_lib = [cenario(lib, "todas as equipes -1 (minimo 1)")["otimo_comprovado"], True,
                 cenario(lib, "todas as equipes +1")["otimo_comprovado"]]
    for bars, provas in ((b1, prova_lib), (b2, prova_livre)):
        for r, ok in zip(bars, provas):
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 4,
                    f"{int(r.get_height())}" + ("" if ok else "*"),
                    ha="center", fontsize=14, fontweight="bold")
    if not all(prova_livre + prova_lib):
        ax.text(1.0, -0.2, "* limite superior (sem prova de ótimo)", transform=ax.transAxes,
                ha="right", fontsize=11, color=TINTA_2)
    ax.set_xticks(list(x), grupos)
    ax.set_ylim(0, 330)
    ax.set_ylabel("prazo (dias)")
    ax.yaxis.grid(True, color=GRADE, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    ax.legend(frameon=False, fontsize=13, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.12))
    salvar(fig, "05-equipes.png")


def main():
    d, nome = ultima_rodada()
    print("rodada:", nome)
    g1_prazos(d)
    g2_sensibilidade(d)
    g3_curva(d)
    g4_gantt(d)
    g5_equipes(d)


if __name__ == "__main__":
    main()
