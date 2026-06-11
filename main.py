import random
import time
import statistics
import sys

sys.setrecursionlimit(200000)


# ALGORITMOS DE ORDENAÇÃO

def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        trocou = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True

        if not trocou:
            break

    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = chave

    return arr


def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        menor = i

        for j in range(i + 1, n):
            if arr[j] < arr[menor]:
                menor = j

        arr[i], arr[menor] = arr[menor], arr[i]

    return arr


def heap_sort(arr):
    n = len(arr)

    def heapify(arr, n, i):
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2

        if esquerda < n and arr[esquerda] > arr[maior]:
            maior = esquerda

        if direita < n and arr[direita] > arr[maior]:
            maior = direita

        if maior != i:
            arr[i], arr[maior] = arr[maior], arr[i]
            heapify(arr, n, maior)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr


def shell_sort(arr):
    n = len(arr)
    intervalo = n // 2

    while intervalo > 0:
        for i in range(intervalo, n):
            temp = arr[i]
            j = i

            while j >= intervalo and arr[j - intervalo] > temp:
                arr[j] = arr[j - intervalo]
                j -= intervalo

            arr[j] = temp

        intervalo //= 2

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    meio = len(arr) // 2
    esquerda = merge_sort(arr[:meio])
    direita = merge_sort(arr[meio:])

    i = 0
    j = 0
    resultado = []

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    arr[:] = resultado
    return arr


def quick_sort(arr):
    def particionar(arr, inicio, fim):
        meio = (inicio + fim) // 2
        pivo = arr[meio]

        i = inicio
        j = fim

        while i <= j:
            while arr[i] < pivo:
                i += 1

            while arr[j] > pivo:
                j -= 1

            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        return i

    def quick_sort_rec(arr, inicio, fim):
        if inicio < fim:
            indice = particionar(arr, inicio, fim)

            if inicio < indice - 1:
                quick_sort_rec(arr, inicio, indice - 1)

            if indice < fim:
                quick_sort_rec(arr, indice, fim)

    quick_sort_rec(arr, 0, len(arr) - 1)
    return arr


# GERAÇÃO DOS CENÁRIOS

def gerar_crescente(n):
    return list(range(n))


def gerar_decrescente(n):
    return list(range(n, 0, -1))


def gerar_aleatorio_sem_repetidos(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr


def gerar_aleatorio_com_repetidos(n):
    return [random.randint(0, n // 2) for _ in range(n)]


# CÁLCULO ESTATÍSTICO

def calcular_media_filtrada(tempos):
    media = statistics.mean(tempos)
    variancia = statistics.variance(tempos)
    desvio_padrao = statistics.stdev(tempos)

    limite_inferior = media - desvio_padrao
    limite_superior = media + desvio_padrao

    tempos_validos = []

    for tempo in tempos:
        if limite_inferior <= tempo <= limite_superior:
            tempos_validos.append(tempo)

    media_filtrada = statistics.mean(tempos_validos)

    return {
        "media": media,
        "variancia": variancia,
        "desvio_padrao": desvio_padrao,
        "media_filtrada": media_filtrada,
        "tempos_validos": tempos_validos
    }



# MEDIÇÃO DE TEMPO


def medir_tempo(algoritmo, array_original):
    copia = array_original.copy()

    inicio = time.perf_counter_ns()
    algoritmo(copia)
    fim = time.perf_counter_ns()

    return fim - inicio


# EXECUÇÃO DOS TESTES

def executar_testes():
    tamanhos = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]

    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Heap Sort": heap_sort,
        "Shell Sort": shell_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    cenarios = {
        "Array crescente sem valores repetidos": gerar_crescente,
        "Array decrescente sem valores repetidos": gerar_decrescente,
        "Array aleatorio sem valores repetidos": gerar_aleatorio_sem_repetidos,
        "Array aleatorio com valores repetidos": gerar_aleatorio_com_repetidos
    }

    resultados = {}

    for nome_cenario, funcao_geradora in cenarios.items():
        print(f"\nExecutando cenário: {nome_cenario}")
        resultados[nome_cenario] = {}

        for n in tamanhos:
            print(f"  Tamanho do array: {n}")
            array_original = funcao_geradora(n)

            resultados[nome_cenario][n] = {}

            for nome_algoritmo, algoritmo in algoritmos.items():
                print(f"    Testando {nome_algoritmo}...")

                tempos = []

                for execucao in range(10):
                    tempo = medir_tempo(algoritmo, array_original)
                    tempos.append(tempo)

                dados = calcular_media_filtrada(tempos)

                resultados[nome_cenario][n][nome_algoritmo] = round(dados["media_filtrada"])

    return resultados, tamanhos, algoritmos.keys()


# GERAÇÃO DO ARQUIVO MARKDOWN


def gerar_markdown(resultados, tamanhos, nomes_algoritmos):
    with open("resultados.md", "w", encoding="utf-8") as arquivo:
        arquivo.write("# Análise Comparativa dos Métodos de Ordenação\n\n")

        arquivo.write("## Informações do experimento\n\n")
        arquivo.write("- Linguagem utilizada: Python\n")
        arquivo.write("- Medição de tempo: `time.perf_counter_ns()`\n")
        arquivo.write("- Unidade de tempo: nanossegundos\n")
        arquivo.write("- Quantidade de execuções por teste: 10\n")
        arquivo.write("- Critério estatístico: média, variância, desvio padrão e média filtrada usando média ± desvio padrão\n\n")

        arquivo.write("## Algoritmos implementados\n\n")
        arquivo.write("- Bubble Sort\n")
        arquivo.write("- Insertion Sort\n")
        arquivo.write("- Selection Sort\n")
        arquivo.write("- Heap Sort\n")
        arquivo.write("- Shell Sort\n")
        arquivo.write("- Merge Sort\n")
        arquivo.write("- Quick Sort\n\n")

        for nome_cenario, dados_cenario in resultados.items():
            arquivo.write(f"## {nome_cenario}\n\n")

            cabecalho = "| Tamanho do Array (n) | " + " | ".join(nomes_algoritmos) + " |\n"
            separador = "|---:|" + "|".join(["---:" for _ in nomes_algoritmos]) + "|\n"

            arquivo.write(cabecalho)
            arquivo.write(separador)

            for n in tamanhos:
                linha = f"| {n} | "

                valores = []
                for nome_algoritmo in nomes_algoritmos:
                    valores.append(str(dados_cenario[n][nome_algoritmo]))

                linha += " | ".join(valores) + " |\n"
                arquivo.write(linha)

            arquivo.write("\n")

        arquivo.write("## Metodologia de cálculo dos tempos\n\n")
        arquivo.write("Para cada combinação de cenário, tamanho de array e algoritmo de ordenação, foram realizadas 10 execuções. Em cada execução, o tempo foi medido em nanossegundos usando `time.perf_counter_ns()`.\n")
        
        arquivo.write("Após as 10 execuções, foi calculada a média dos tempos. Em seguida, foi calculada a variância amostral e o desvio padrão. Com base no desvio padrão, foram desconsiderados os valores que ficaram fora do intervalo média ± desvio padrão..\n\n")

        arquivo.write("Os valores apresentados nas tabelas correspondem à média final filtrada, calculada somente com os tempos que permaneceram dentro desse intervalo.")
       

if __name__ == "__main__":
    resultados, tamanhos, nomes_algoritmos = executar_testes()
    gerar_markdown(resultados, tamanhos, nomes_algoritmos)

    print("\nTestes finalizados.")
    print("Arquivo resultados.md gerado com sucesso.")
