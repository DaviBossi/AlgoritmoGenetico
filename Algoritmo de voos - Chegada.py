#Trabalho de GA - Inteligencia Artificial
#Davi Pereira Bossi - 2018000926

import random
# Funcao para criar cada individuo
def criar_individuo():
    with open('flights.txt','r') as arquivo:
        voos = arquivo.readlines()

    voos = [voo.strip() for voo in voos]  # Remove os caracteres de quebra de linha

    voos_destino_fco = [voo for voo in voos if voo.split(",")[1] == "FCO"]  # Filtra os voos com destino "FCO"

    individuo = []
    origens = []

    while len(individuo) < 6:
        voo = random.choice(voos_destino_fco)  # Seleciona aleatoriamente um voo de destino "FCO"
        origem = voo.split(",")[0]  # Obtém a cidade de origem do voo
        if origem not in origens and origem not in individuo:  # Verifica se a cidade de origem já existe no indivíduo
            individuo.append(voo)
            origens.append(origem)

    return individuo

#Funcao para criar a populacao
def criar_populacao(tamanho_populacao):
    populacao = [] # Cria uma lista vazia para armazenar a populacao
    for _ in range(tamanho_populacao):
        individuo = criar_individuo() # Cria cada individuo 
        populacao.append(individuo) # Adiciona o individuo criado a populacao
        
    return populacao

#Transforma horas em minutos para facilitar o calculo
def calcular_minutos(horario):
    horas, minutos = horario.split(":") 
    return int(horas) * 60 + int(minutos)

#Funcao para calcular fitness
def calcular_fitness(individuo):
    chegada_voos = [voo.split(",")[3] for voo in individuo]  # Obtém os horários de chegada de todos os voos
    tempos_chegada = [calcular_minutos(chegada) for chegada in chegada_voos]  # Converte os horários de chegada em minutos

    tempo_mais_cedo = min(tempos_chegada)  # Encontra o tempo de chegada mais cedo
    tempo_mais_tarde = max(tempos_chegada)  # Encontra o tempo de chegada mais tarde

    diferenca_minutos = tempo_mais_tarde - tempo_mais_cedo
    
    preco_passagem = [int(voo.split(",")[4]) for voo in individuo] # Obtem o preco de as passagens de todos os voos
    media_passagem = sum(preco_passagem)/6 #Encontra o preço medio de todas as passagens 
     
    return -(diferenca_minutos + media_passagem)   # Retornamos o valor negativo para que a menor diferença de tempo tenha um fitness maior

#Funcao para selecionar os pais dentro da populacao
def selecionar_pais(populacao):
    pai1 = random.choice(populacao)
    pai2 = random.choice(populacao) 
    
    return pai1,pai2

#Funcao para cruzar os dois pais selecionados
def cruzar(pais1, pais2):
    ponto_corte = random.randint(1, len(pais1) - 1) #Seleciona um ponto de corte aleatório
    
    # Realiza o cruzamento do DNA dos pais
    filho1 = pais1[:ponto_corte] + pais2[ponto_corte:]
    filho2 = pais2[:ponto_corte] + pais1[ponto_corte:]
    
    return filho1, filho2

#Funcao para mutar o individuo
def mutar(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            # Gera um novo voo aleatório para substituir o voo atual
            novo_voo = gerar_voo_aleatorio(individuo)
            individuo[i] = novo_voo

    return individuo

#Funcao para gerar um voo aleatorio que sera usado na mutacao
def gerar_voo_aleatorio(individuo):
    origens = [voo.split(",")[0] for voo in individuo] #Pega a origem do voo no individuo
    destinos = [voo.split (",")[1] for voo in individuo] #Pega o destino do voo no individuo

    # Lê o arquivo de voos
    with open('flights.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    voos_disponiveis = []
    for linha in linhas:
        voo = linha.strip()
        origem, destino, _, _, _ = voo.split(',')

        # Verifica se a origem é válida e não está presente no indivíduo
        if origem in origens and destino in destinos and voo not in individuo:
            voos_disponiveis.append(voo)

    if not voos_disponiveis:
        # Caso não existam voos disponíveis, retorna None
        return None

    voo_aleatorio = random.choice(voos_disponiveis)
    return voo_aleatorio

#Funcao para substituir os voos com o mesmo destino nos individuos
def substituir_voos_repetidos(individuo):
    origens_presentes = []
    origens_disponiveis = []
    with open('flights.txt','r') as arquivo:
        voos = arquivo.readlines()

    voos = [voo.strip() for voo in voos]  # Remove os caracteres de quebra de linha

    voos_disponiveis = [voo for voo in voos if voo.split(",")[1] == "FCO"]  # Filtra os voos com destino "FCO"

    # Verifica as origens presentes nos voos disponiveis
    for voo in voos_disponiveis:
        origem, _, _, _, _ = voo.split(',')
        origens_disponiveis.append(origem)
    new_origens = set(origens_disponiveis)
    
    # Verifica as origens presentes no indivíduo
    for voo in individuo:
        origem, _, _, _, _ = voo.split(',')
        origens_presentes.append(origem)

    # Percorre o indivíduo e substitui voos repetidos
    for i in range(len(individuo)):
        origem, _, _, _, _ = individuo[i].split(',')
        if origens_presentes.count(origem) > 1:
            # Remove o voo repetido
            individuo.pop(i)
            
            # Verifica qual origem está faltando no indivíduo
            origem_faltando = [origem for origem in new_origens if origem not in origens_presentes]
            
            # Se houver origem faltando, adiciona um novo voo aleatório com essa origem
            if origem_faltando:
                voos_origem_faltando = [voo for voo in voos_disponiveis if voo.startswith(origem_faltando[0])]
                novo_voo = random.choice(voos_origem_faltando)
                individuo.insert(i, novo_voo)
            
            # Atualiza a lista de origens presentes no indivíduo
            origens_presentes = [v.split(',')[0] for v in individuo]

    return individuo

#Funcao para gerar a nova populacao depois dos cruzamentos e mutacoes
def evoluir_populacao(populacao, taxa_mutacao):
    nova_populacao = []
    # Seleciona os pais, realiza o cruzamento e a mutação para gerar a nova população
    for _ in range(len(populacao)):
        pai1,pai2 = selecionar_pais(populacao) 
        filho1, filho2 = cruzar(pai1, pai2)
        filho1 = mutar(filho1, taxa_mutacao)
        filho2 = mutar(filho2, taxa_mutacao)
        filho1 = substituir_voos_repetidos(filho1)
        filho2 = substituir_voos_repetidos(filho2)
        nova_populacao.extend([filho1, filho2])
    
    return nova_populacao

#Funcao para encontrar o melhor individuo
def encontrar_melhor_individuo(populacao):
    melhor_individuo = None
    melhor_fitness = float('-inf')

    for individuo in populacao:
        fitness = calcular_fitness(individuo)

        if fitness > melhor_fitness:
            melhor_fitness = fitness
            melhor_individuo = individuo

    return melhor_individuo, melhor_fitness

#Parametros do GA
tamanho_populacao = 15
taxa_mutacao = 0.15
numero_geracoes = 15

populacao = criar_populacao(tamanho_populacao)

#Criar todas as populacoes de acordo com o parametros passados
for geracao in range(numero_geracoes):
    populacao = evoluir_populacao(populacao, taxa_mutacao)
    melhor_individuo, melhor_fitness = encontrar_melhor_individuo(populacao)
    print("Geração:", geracao+1, "Melhor fitness:", melhor_fitness)

# Exibir o melhor indivíduo encontrado
print("Melhor indivíduo encontrado:", melhor_individuo)


    
    