import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Definições iniciais
num_rodadas = 5000
fc_values = np.linspace(0.50, 0.75, 25)

# Definir os prêmios e o RTP desejado
premios = [500, 200, 100, 50, 20, 10, 5, 2]
rtp_desejado = 0.75

# Calcular a contribuição igualitária de cada prêmio para o RTP
n = len(premios)
contribuicao_igual = rtp_desejado / n

# Calcular as probabilidades para cada prêmio
probabilidades = [contribuicao_igual / premio for premio in premios]

# Normalizar as probabilidades para que somem 1
soma_probabilidades = sum(probabilidades)
probabilidades = [p / soma_probabilidades for p in probabilidades]

# Função para simular rodadas com ajuste de RTP
def simular_rodadas(fc):
    ganhos = []
    apostas = np.ones(num_rodadas)  # Aposta constante de 1 unidade por rodada
    rtp_acumulado = []

    for i in range(num_rodadas):
        ganho = np.random.choice(premios, p=probabilidades)
        ganhos.append(ganho)

        if i > 0:
            rtp_atual = np.sum(ganhos) / np.sum(apostas[:i + 1])
            ajuste = (rtp_desejado - rtp_atual) * np.sum(apostas[:i + 1]) / fc
            ganhos[-1] = max(0, ganho + ajuste)

        rtp_acumulado.append(np.sum(ganhos) / np.sum(apostas[:i + 1]))

    lucro_acumulado = np.cumsum(apostas) - np.cumsum(ganhos)
    return np.array(rtp_acumulado), np.array(lucro_acumulado)

# Inicialização das listas para armazenar resultados
rtp_finais = []
lucros_finais = []

# Gerar gráficos para cada simulação de FC
for fc in fc_values:
    rtp_evolucao, lucro_acumulado = simular_rodadas(fc)

    # Guardar estatísticas do RTP e lucro
    rtp_finais.append(rtp_evolucao[-1])
    lucros_finais.append(lucro_acumulado[-1])

    # Gráfico da evolução do RTP
    plt.figure()
    plt.plot(rtp_evolucao)
    plt.title(f'Evolução do RTP - FC={fc:.2f}')
    plt.xlabel('Rodadas')
    plt.ylabel('RTP Acumulado')
    plt.grid(True)
    plt.savefig(f'rtp_evolucao_fc_{fc:.2f}.png')
    plt.close()

    # Gráfico do lucro acumulado
    plt.figure()
    plt.plot(lucro_acumulado)
    plt.title(f'Lucro Acumulado - FC={fc:.2f}')
    plt.xlabel('Rodadas')
    plt.ylabel('Lucro Acumulado')
    plt.grid(True)
    plt.savefig(f'lucro_acumulado_fc_{fc:.2f}.png')
    plt.close()

# Gráfico do RTP final por simulação de FC
plt.figure()
plt.plot(fc_values, rtp_finais, label='RTP Final', marker='o')
plt.title('RTP Final por Simulação de FC')
plt.xlabel('Fator de Correção (FC)')
plt.ylabel('RTP Final')
plt.grid(True)
plt.savefig('rtp_final_por_fc.png')
plt.close()

# Gráfico do lucro final por simulação de FC
plt.figure()
plt.plot(fc_values, lucros_finais, label='Lucro Final', marker='o')
plt.title('Lucro Final por Simulação de FC')
plt.xlabel('Fator de Correção (FC)')
plt.ylabel('Lucro Final')
plt.grid(True)
plt.savefig('lucro_final_por_fc.png')
plt.close()

# Criação do PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Função para adicionar gráficos ao PDF
def adicionar_grafico_ao_pdf(pdf, titulo, caminho_imagem):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align='C')
    pdf.image(caminho_imagem, x=10, y=30, w=190)

# Adicionar gráficos ao PDF
for fc in fc_values:
    adicionar_grafico_ao_pdf(pdf, f'Evolução do RTP - FC={fc:.2f}', f'rtp_evolucao_fc_{fc:.2f}.png')
    adicionar_grafico_ao_pdf(pdf, f'Lucro Acumulado - FC={fc:.2f}', f'lucro_acumulado_fc_{fc:.2f}.png')

adicionar_grafico_ao_pdf(pdf, 'RTP Final por Simulação de FC', 'rtp_final_por_fc.png')
adicionar_grafico_ao_pdf(pdf, 'Lucro Final por Simulação de FC', 'lucro_final_por_fc.png')

# Salvar o PDF
pdf.output("relatorio_simulacao.pdf")

print("Relatório gerado com sucesso: relatorio_simulacao.pdf")
