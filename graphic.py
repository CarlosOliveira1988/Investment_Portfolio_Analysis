
import matplotlib.pyplot as plt  # Importação da biblioteca Matplotlib

x = ['a', 'b', 'c', 'd']
y1 = [1, 2, 3, 4]
y2 = [5, 6, 7, 8]

table = [x, y1, y2]
n = [['S1'], ['S2']]

# Plota valor da operação
for i in range(1, len(table)):
    plt.plot(table[0], table[i], label=n[i-1])
    # plt.legend(n[i-1])


plt.legend(loc="upper left")
plt.ylabel('Valor da operação')
plt.xlabel('Data')
plt.show()
