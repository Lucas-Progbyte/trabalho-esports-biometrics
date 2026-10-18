
import csv
import os
import random


PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "dados", "esports_gaming_biometrics_250k.csv")
PASTA_GRAFICOS = os.path.join(PASTA, "graficos")


COLUNAS_INT = ["Age", "Energy_Drinks", "APM", "Heart_Rate_BPM"]
COLUNAS_FLOAT = ["PlayTime_Hours", "Sleep_Hours", "Screen_Brightness",
                 "HRV_Score", "Reaction_Time_ms"]


def carregar_dados(caminho):
   
    dados = []  # lista que guardará todos os registros
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)  # cada linha vira um dict
        for linha in leitor:
            for col in COLUNAS_INT:
                linha[col] = int(linha[col])
            for col in COLUNAS_FLOAT:
                linha[col] = float(linha[col]) if linha[col] != "" else None
            dados.append(linha)
    return dados



def media(valores):
  
    validos = [v for v in valores if v is not None]
    if len(validos) == 0:
        return 0.0
    return sum(validos) / len(validos)


def agrupar(registros, coluna):
    
    grupos = {}
    for r in registros:
        chave = r[coluna]
        if chave not in grupos:
            grupos[chave] = []
        grupos[chave].append(r)
    return grupos


def resumo(registros):
    vitorias = 0
    for r in registros:
        if r["Match_Outcome"] == "Win":
            vitorias += 1
    total = len(registros)
    return {
        "quantidade": total,
        "apm_medio": media([r["APM"] for r in registros]),
        "reacao_media": media([r["Reaction_Time_ms"] for r in registros]),
        "bpm_medio": media([r["Heart_Rate_BPM"] for r in registros]),
        "taxa_vitoria": (vitorias / total * 100) if total > 0 else 0.0,
    }


def ler_inteiro(texto, minimo, maximo):
   
    while True:
        entrada = input(texto).strip()
        if entrada.isdigit() and minimo <= int(entrada) <= maximo:
            return int(entrada)
        print(f"  Entrada inválida. Digite um número entre {minimo} e {maximo}.")


def ler_numero(texto, padrao):
    
    while True:
        entrada = input(texto).strip().replace(",", ".")
        if entrada == "":
            return padrao
        try:
            return float(entrada)
        except ValueError:
            print("  Entrada inválida. Digite um número (ou Enter para o padrão).")


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)



def acao_1_agrupar(dados):
    titulo("AÇÃO 1 - AGRUPAMENTO (ordenado por quantidade de sessões)")
    opcoes = {1: ("Game_Genre", "Gênero do jogo"),
              2: ("Age", "Idade do jogador"),
              3: ("Blue_Light_Filter", "Filtro de luz azul")}
    for numero, (coluna, nome) in opcoes.items():
        print(f"  {numero} - Agrupar por {nome} ({coluna})")
    escolha = ler_inteiro("Escolha o agrupamento: ", 1, 3)
    coluna, nome = opcoes[escolha]

    grupos = agrupar(dados, coluna)           

  
    linhas = []
    for chave, registros in grupos.items():
        estat = resumo(registros)
        estat["grupo"] = chave
        linhas.append(estat)

  
    linhas = sorted(linhas, key=lambda x: x["quantidade"], reverse=True)

    print(f"\nTotal de grupos encontrados: {len(linhas)}")
    if len(linhas) > 10:
        print("(Exibindo apenas o Top 10)")
        linhas = linhas[:10]

    print(f"\n{nome:<18}{'Qtd':>9}{'APM médio':>12}{'Reação(ms)':>13}{'BPM médio':>12}{'Vitórias %':>12}")
    print("-" * 76)
    for l in linhas:
        print(f"{str(l['grupo']):<18}{l['quantidade']:>9}{l['apm_medio']:>12.1f}"
              f"{l['reacao_media']:>13.1f}{l['bpm_medio']:>12.1f}{l['taxa_vitoria']:>11.1f}%")



def acao_2_top10(dados):
    titulo("AÇÃO 2 - TOP 10 JOGADORES")
  
    metricas = {1: ("APM", "Maior APM (ações por minuto)", True),
                2: ("Reaction_Time_ms", "Menor tempo de reação (mais rápido)", False),
                3: ("HRV_Score", "Maior HRV (menos estresse fisiológico)", True)}
    for numero, (coluna, descricao, _) in metricas.items():
        print(f"  {numero} - {descricao}")
    escolha = ler_inteiro("Escolha a métrica: ", 1, 3)
    coluna, descricao, decrescente = metricas[escolha]

    
    validos = [r for r in dados if r[coluna] is not None]

    
    ordenados = sorted(validos, key=lambda r: r[coluna], reverse=decrescente)
    top10 = ordenados[:10]

    print(f"\nTop 10 - {descricao}\n")
    print(f"{'#':<4}{'Player_ID':<12}{'Gênero':<15}{'Idade':>6}{'APM':>6}"
          f"{'Reação':>9}{'BPM':>6}{'HRV':>8}{'Resultado':>11}")
    print("-" * 77)
    for posicao, r in enumerate(top10, start=1):
        hrv = f"{r['HRV_Score']:.1f}" if r["HRV_Score"] is not None else "-"
        print(f"{posicao:<4}{r['Player_ID']:<12}{r['Game_Genre']:<15}{r['Age']:>6}{r['APM']:>6}"
              f"{r['Reaction_Time_ms']:>9.1f}{r['Heart_Rate_BPM']:>6}{hrv:>8}{r['Match_Outcome']:>11}")



def acao_3_comparar(dados):
    titulo("AÇÃO 3 - COMPARAR GÊNEROS DE JOGO")
    grupos = agrupar(dados, "Game_Genre")
    generos = sorted(grupos.keys())           

    for i, g in enumerate(generos, start=1):
        print(f"  {i} - {g}")

    while True:
        entrada = input("Digite 2 ou mais números separados por vírgula (ex: 1,3): ")
        escolhidos = []
        valido = True
        for parte in entrada.split(","):
            parte = parte.strip()
            if parte.isdigit() and 1 <= int(parte) <= len(generos):
                nome = generos[int(parte) - 1]
                if nome not in escolhidos:   
                    escolhidos.append(nome)
            else:
                valido = False
        if valido and len(escolhidos) >= 2:
            break
        print("  Entrada inválida. Escolha pelo menos 2 opções diferentes.")

    resultados = {g: resumo(grupos[g]) for g in escolhidos}

    print(f"\n{'Gênero':<16}{'Qtd':>9}{'APM médio':>12}{'Reação(ms)':>13}{'BPM médio':>12}{'Vitórias %':>12}")
    print("-" * 74)
    for g, e in resultados.items():
        print(f"{g:<16}{e['quantidade']:>9}{e['apm_medio']:>12.1f}{e['reacao_media']:>13.1f}"
              f"{e['bpm_medio']:>12.1f}{e['taxa_vitoria']:>11.1f}%")

    
    maior_apm = max(resultados, key=lambda g: resultados[g]["apm_medio"])
    menor_reacao = min(resultados, key=lambda g: resultados[g]["reacao_media"])
    maior_vit = max(resultados, key=lambda g: resultados[g]["taxa_vitoria"])
    print(f"\n-> Maior APM médio: {maior_apm}")
    print(f"-> Menor tempo de reação médio: {menor_reacao}")
    print(f"-> Maior taxa de vitórias: {maior_vit}")



def acao_4_conjuntos(dados):
    titulo("AÇÃO 4 - CONJUNTOS: SONO E ENERGÉTICOS")
    print("Conjunto A = jogadores que dormiram POUCO (menos de X horas)")
    print("Conjunto B = jogadores que consumiram MUITO energético (X ou mais)")
    limite_sono = ler_numero("Limite de sono em horas [Enter = 5]: ", 5.0)
    limite_energ = ler_numero("Mínimo de energéticos [Enter = 2]: ", 2.0)

    
    conjunto_a = set()
    conjunto_b = set()
    for r in dados:
        if r["Sleep_Hours"] < limite_sono:
            conjunto_a.add(r["Player_ID"])
        if r["Energy_Drinks"] >= limite_energ:
            conjunto_b.add(r["Player_ID"])

    uniao = conjunto_a | conjunto_b          
    intersecao = conjunto_a & conjunto_b    
    so_a = conjunto_a - conjunto_b           
    so_b = conjunto_b - conjunto_a           

    
    indice = {r["Player_ID"]: r for r in dados}

    operacoes = [
        ("A  (dormiu pouco)", conjunto_a),
        ("B  (muito energético)", conjunto_b),
        ("A ∪ B (união)", uniao),
        ("A ∩ B (interseção)", intersecao),
        ("A - B (diferença)", so_a),
        ("B - A (diferença)", so_b),
    ]

    print(f"\n{'Conjunto':<24}{'Jogadores':>10}{'Reação(ms)':>13}{'APM médio':>11}{'Vitórias %':>12}")
    print("-" * 70)
    for nome, conjunto in operacoes:
        registros = [indice[pid] for pid in conjunto]
        e = resumo(registros)
        print(f"{nome:<24}{len(conjunto):>10}{e['reacao_media']:>13.1f}"
              f"{e['apm_medio']:>11.1f}{e['taxa_vitoria']:>11.1f}%")

    # Conjunto de gêneros (valores únicos) presentes na interseção
    generos = set(indice[pid]["Game_Genre"] for pid in intersecao)
    print(f"\nGêneros presentes em A ∩ B: {', '.join(sorted(generos)) if generos else 'nenhum'}")



def importar_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("matplotlib não instalado. Execute: pip install matplotlib")
        return None


def finalizar_grafico(plt, nome_arquivo):
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, nome_arquivo)
    plt.tight_layout()
    plt.savefig(caminho, dpi=120)
    print(f"Gráfico salvo em: {caminho}")
    plt.show()
    plt.close()


def gerar_grafico_1(dados):
    
    plt = importar_matplotlib()
    if plt is None:
        return
    grupos = agrupar(dados, "Game_Genre")
    medias = {g: media([r["APM"] for r in regs]) for g, regs in grupos.items()}

    ordem = sorted(medias, key=lambda g: medias[g], reverse=True)
    valores = [medias[g] for g in ordem]

    plt.figure(figsize=(8, 5))
    barras = plt.bar(ordem, valores, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])
    for barra, v in zip(barras, valores):
        plt.text(barra.get_x() + barra.get_width() / 2, v + 2, f"{v:.1f}", ha="center")
    plt.title("APM médio por gênero de jogo")
    plt.xlabel("Gênero do jogo (Game_Genre)")
    plt.ylabel("APM médio (ações por minuto)")
    finalizar_grafico(plt, "grafico_1_apm_por_genero.png")


def gerar_grafico_2(dados):
   
    plt = importar_matplotlib()
    if plt is None:
        return
  
    random.seed(42)
    amostra = random.sample(dados, 3000)
    x = [r["Sleep_Hours"] for r in amostra]
    y = [r["Reaction_Time_ms"] for r in amostra]

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, s=8, alpha=0.4, color="#4C72B0")
    plt.title("Horas de sono x Tempo de reação (amostra de 3000 sessões)")
    plt.xlabel("Horas de sono na noite anterior (Sleep_Hours)")
    plt.ylabel("Tempo de reação em ms (Reaction_Time_ms)")
    plt.grid(alpha=0.3)
    finalizar_grafico(plt, "grafico_2_sono_vs_reacao.png")



def mostrar_menu():
    print("\n" + "=" * 40)
    print("     E-SPORTS BIOMETRICS ANALYZER")
    print("=" * 40)
    print("1 - Agrupar dados (gênero/idade/filtro) ordenados")
    print("2 - Top 10 jogadores (APM / reação / HRV)")
    print("3 - Comparar gêneros de jogo")
    print("4 - Análise com conjuntos (sono x energéticos)")
    print("5 - Gráfico de barras: APM médio por gênero")
    print("6 - Gráfico de dispersão: sono x tempo de reação")
    print("0 - Sair")


def main():
    if not os.path.exists(ARQUIVO_CSV):
        print(f"Arquivo não encontrado: {ARQUIVO_CSV}")
        return
    print("Carregando dados...")
    dados = carregar_dados(ARQUIVO_CSV)
    print(f"{len(dados)} registros carregados.")

    acoes = {"1": acao_1_agrupar, "2": acao_2_top10, "3": acao_3_comparar,
             "4": acao_4_conjuntos, "5": gerar_grafico_1, "6": gerar_grafico_2}

    try:
        while True:
            mostrar_menu()
            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "0":
                print("Encerrando. Até logo!")
                break
            if opcao in acoes:
                acoes[opcao](dados)
            else:
                print("Opção inválida! Digite um número de 0 a 6.")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()
